#include <unistd.h>
#include <string.h>
#include <stdlib.h>
#include <dlfcn.h>
#include <stdio.h>
#include <stdbool.h>
#include <net/if.h>

#define SIOCGIFHWADDR 0x8927

typedef int (*ioctl_t)(int fd, unsigned long request, unsigned long arg);

ioctl_t lib_ioctl;

void do_redirect() {
	void *libc;
	char *error;

	if (!(libc = dlopen("libc.so.6", RTLD_LAZY))) {
		fprintf(stderr, "Cannot open libc.so.6: %s\n", dlerror());
		exit(1);
	}

	lib_ioctl = dlsym(libc, "ioctl");

	if ((error = dlerror()) != NULL) {
		fprintf(stderr, "%s\n", error);
		exit(1);
	}
}

char *straddr(char *hwaddr) {
	char *text = malloc(IFHWADDRLEN*3*sizeof(char));
	for (int byte=0; byte<IFHWADDRLEN; byte++) {
		char octet[4]; // includes null terminator
		sprintf(octet, "%02x:", hwaddr[byte] & 0xff);
		strncpy(&text[byte*3], octet, 3); // exclude the terminating null
	}
	text[IFHWADDRLEN*3-1] = '\0'; // replace the last colon with the terminating null
	return text;
}

int ioctl(int fd, unsigned long request, unsigned long arg) {
	int i;
	char var[IFNAMSIZ+8], *endptr;
	const char *hwtxt, *ptr;
	const bool debug=(getenv("FAKEIF_DEBUG") != NULL);

	if (!lib_ioctl)
		do_redirect();

	// actually make the call so we have valid values and only overwrite
	// the hwaddr in the response
	i = lib_ioctl(fd, request, arg);
	if (i < 0)
		return i;

	if (request == SIOCGIFHWADDR) {
		if (debug)
			fprintf(stderr, "SIOCGIFHWADDR intercepted\n");
		struct ifreq *req=(struct ifreq *)arg;
		sprintf(var, "HWADDR_%.*s", IFNAMSIZ, req->ifr_name);
		if ((hwtxt=getenv(var)) != NULL) {
			if (debug)
				fprintf(stderr, "Old MAC address %s\n", straddr(req->ifr_ifru.ifru_hwaddr.sa_data));

			fprintf(stderr, "Replacing original address %s of %s with %s\n", straddr(req->ifr_ifru.ifru_hwaddr.sa_data), req->ifr_name, hwtxt);

			char new_addr[6];
			if (6 != sscanf(hwtxt, "%02hhx:%02hhx:%02hhx:%02hhx:%02hhx:%02hhx%*c",
						&new_addr[0], &new_addr[1], &new_addr[2],
						&new_addr[3], &new_addr[4], &new_addr[5])) {
				fprintf(stderr, "Invalid MAC address %s\n", hwtxt);
				return i;
			}
			memcpy(&req->ifr_ifru.ifru_hwaddr.sa_data, new_addr, 6);
			if (debug)
				fprintf(stderr, "New MAC address %s\n", straddr(req->ifr_ifru.ifru_hwaddr.sa_data));
		} else {
			if (debug)
				fprintf(stderr, "No override for %s\n", req->ifr_name);
		}
	}

	if (debug)
		fprintf(stderr, "ioctl hooked: returns %d\n", i);

	return i;
}
