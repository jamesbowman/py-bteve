// Include the header file to get access to the MicroPython API
#include "py/dynruntime.h"

mp_obj_type_t stem_type;

typedef struct _mp_obj_stem_t {
    mp_obj_base_t base;
    mp_obj_t writer;

    uint8_t buf[512];
    size_t n;
} mp_obj_stem_t;

mp_map_elem_t stem_locals_dict_table[3];
STATIC MP_DEFINE_CONST_DICT(stem_locals_dict, stem_locals_dict_table);

STATIC void stem_print(const mp_print_t *print,
    mp_obj_t self_in,
    mp_print_kind_t kind)
{
    mp_printf(print, "bteve stem");
}

STATIC mp_obj_t stem_make_new(
    const mp_obj_type_t *type,
    size_t n_args,
    size_t n_kw,
    const mp_obj_t *args)
{
    mp_obj_stem_t *o = m_new_obj(mp_obj_stem_t);
    o->base.type = type;
    return o;
}

STATIC mp_obj_t _register(mp_obj_t self, mp_obj_t o) {
    mp_obj_stem_t *stem = self;
    stem->writer = o;
    return mp_const_none;
}
STATIC MP_DEFINE_CONST_FUN_OBJ_2(register_obj, _register);

STATIC mp_obj_t _flush(mp_obj_t self) {
    mp_obj_stem_t *stem = self;

    mp_obj_t args[1] = {
      mp_obj_new_bytearray_by_ref(stem->n, stem->buf)
    };
    mp_call_function_n_kw(stem->writer, 1, 0, &args[0]);
    return mp_const_none;
}
STATIC MP_DEFINE_CONST_FUN_OBJ_1(flush_obj, _flush);

#define APPEND4(u) \
  do { \
    mp_obj_stem_t *stem = self; \
    *(uint32_t*)(stem->buf + stem->n) = (u); \
    stem->n += sizeof(uint32_t); \
  } while (0)

STATIC mp_obj_t _pointsize(mp_obj_t self, mp_obj_t a0) {
    APPEND4((0x0d << 24) | (mp_obj_get_int_truncated(a0) & 0x1fff));
    return mp_const_none;
}
STATIC MP_DEFINE_CONST_FUN_OBJ_2(pointsize_obj, _pointsize);

// This is the entry point and is called when the module is imported
mp_obj_t mpy_init(mp_obj_fun_bc_t *self, size_t n_args, size_t n_kw, mp_obj_t *args) {
    MP_DYNRUNTIME_INIT_ENTRY

    stem_type.base.type = &mp_type_type;
    stem_type.name = MP_QSTR_stem;
    stem_type.print = stem_print;
    stem_type.make_new = stem_make_new;
    stem_locals_dict_table[0] = (mp_map_elem_t){ MP_OBJ_NEW_QSTR(MP_QSTR_register), MP_OBJ_FROM_PTR(&register_obj) };
    stem_locals_dict_table[1] = (mp_map_elem_t){ MP_OBJ_NEW_QSTR(MP_QSTR_flush), MP_OBJ_FROM_PTR(&flush_obj) };
    stem_locals_dict_table[2] = (mp_map_elem_t){ MP_OBJ_NEW_QSTR(MP_QSTR_PointSize), MP_OBJ_FROM_PTR(&pointsize_obj) };
    stem_type.locals_dict = (void*)&stem_locals_dict;

    mp_store_global(MP_QSTR_stem, MP_OBJ_FROM_PTR(&stem_type));

    MP_DYNRUNTIME_INIT_EXIT
}
