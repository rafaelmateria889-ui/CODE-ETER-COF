#define _GNU_SOURCE
#include <dlfcn.h>
#include <stdint.h>
/* Testing shim only. Do not ship/preload in the player's installation.
   Virtual CI has no udev/haptic/gamepad hardware. Keep video, audio and events. */
int SDL_Init(uint32_t flags) {
  int (*real_init)(uint32_t) = dlsym(RTLD_NEXT, "SDL_Init");
  return real_init(flags & ~(0x200u | 0x1000u | 0x2000u | 0x8000u));
}
