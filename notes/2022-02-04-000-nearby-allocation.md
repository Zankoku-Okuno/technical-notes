# C: Nearby Allocation of Dynamic Data
tags: c

I saw some example code, which purports to implement something like flexible array members, but a little more flexibly.
Admittedly, compared to a flexible array member, you pay an extra pointer, but the benefit is that you can put as many dynamically-sized buffers as you'd like into a struct, and they don't need to be at the end.
With this strategy, we can arrange for dynamic buffer data to be near in memory to the , thereby likely cutting down the time-to-access, even though there's technically a pointer dereference.

```
struct header {
  size_t len;
  unsigned char *data;
};

struct header *p;
p = malloc(sizeof(*p) + len + 1);
p->data = (unsigned char*)(p + 1); // memory after p is mine!
```

(I'm not sure why the `+ 1` in `malloc`, perhaps this is for NUL-terminated strings specifically?)

There are potential alignment issues of course:
  if `header` is a size that isn't a divisor of the alignment of your dynamic data, you'd have to over-allocate and then align yourself.
This only gets more difficult if you have multiple inline dynamic data members:

```
struct thing {
  size_t len1;
  size_t len2;
  bool isFoo;
  float* nums1;
  double* nums2;
}

thing* alloc_thing(size_t len1, size_t len2) {
  size_t sz = sizeof(thing);          // we need at least this much space for the header
  sz = alignup(sz, alignof(float));   // add padding for alignment
  sz += len1 * sizeof(float);         // put `len1` many floats here
  sz = alignup(sz, alignof(double));  // add padding for alignment
  sz += len2 * sizeof(double);        // put `len2` many doubles here

  size_t al = max(alignof(thing), alignof(float), alignof(double))
  thing* out = aligned_alloc(al, sz);

  out->floats = alignup((char*)(out + 1), alignof(float);
  out->floats = alignup((char*)(&out->floats[len1]), alignof(double));

  out->len1 = len1;
  out->len2 = len2;
  return out;
}
```

or something like that.
I can't say I fully thought it through, and I'm surely abusing notation with `alignup`.
Still, if you encapsulate all this junk, I do think it's at least theoretically possible to get this working according to the standard.
