extern "C" {
	#include <assert.h>
#include <ctype.h>

#pragma once

#include <stdbool.h>
#include <stddef.h>

#if defined(_WIN32) || defined(__CYGWIN__)
#define CWK_EXPORT __declspec(dllexport)
#define CWK_IMPORT __declspec(dllimport)
#elif __GNUC__ >= 4
#define CWK_EXPORT __attribute__((visibility("default")))
#define CWK_IMPORT __attribute__((visibility("default")))
#else
#define CWK_EXPORT
#define CWK_IMPORT
#endif

#if defined(CWK_SHARED)
#if defined(CWK_EXPORTS)
#define CWK_PUBLIC CWK_EXPORT
#else
#define CWK_PUBLIC CWK_IMPORT
#endif
#else
#define CWK_PUBLIC
#endif

  struct cwk_segment
  {
    const char* path;
    const char* segments;
    const char* begin;
    const char* end;
    size_t size;
  };

  enum cwk_segment_type
  {
    CWK_NORMAL,
    CWK_CURRENT,
    CWK_BACK
  };
  enum cwk_path_style
  {
    CWK_STYLE_WINDOWS,
    CWK_STYLE_UNIX
  };

  CWK_PUBLIC size_t cwk_path_get_absolute(const char* base, const char* path,
    char* buffer, size_t buffer_size);

  CWK_PUBLIC size_t cwk_path_get_relative(const char* base_directory,
    const char* path, char* buffer, size_t buffer_size);

  CWK_PUBLIC size_t cwk_path_join(const char* path_a, const char* path_b,
    char* buffer, size_t buffer_size);
  CWK_PUBLIC size_t cwk_path_join_multiple(const char** paths, char* buffer,
    size_t buffer_size);
  CWK_PUBLIC void cwk_path_get_root(const char* path, size_t* length);
  CWK_PUBLIC size_t cwk_path_change_root(const char* path, const char* new_root,
    char* buffer, size_t buffer_size);
  CWK_PUBLIC bool cwk_path_is_absolute(const char* path);
  CWK_PUBLIC bool cwk_path_is_relative(const char* path);
  CWK_PUBLIC void cwk_path_get_basename(const char* path, const char** basename,
    size_t* length);
  CWK_PUBLIC size_t cwk_path_change_basename(const char* path,
    const char* new_basename, char* buffer, size_t buffer_size);
  CWK_PUBLIC void cwk_path_get_dirname(const char* path, size_t* length);
  CWK_PUBLIC bool cwk_path_get_extension(const char* path, const char** extension,
    size_t* length);
  CWK_PUBLIC bool cwk_path_has_extension(const char* path);
  CWK_PUBLIC size_t cwk_path_change_extension(const char* path,
    const char* new_extension, char* buffer, size_t buffer_size);
  CWK_PUBLIC size_t cwk_path_normalize(const char* path, char* buffer,
    size_t buffer_size);
  CWK_PUBLIC size_t cwk_path_get_intersection(const char* path_base,
    const char* path_other);
  CWK_PUBLIC bool cwk_path_get_first_segment(const char* path,
    struct cwk_segment* segment);
  CWK_PUBLIC bool cwk_path_get_last_segment(const char* path,
    struct cwk_segment* segment);
  CWK_PUBLIC bool cwk_path_get_next_segment(struct cwk_segment* segment);
  CWK_PUBLIC bool cwk_path_get_previous_segment(struct cwk_segment* segment);
  CWK_PUBLIC enum cwk_segment_type cwk_path_get_segment_type(
    const struct cwk_segment* segment);
  CWK_PUBLIC size_t cwk_path_change_segment(struct cwk_segment* segment,
    const char* value, char* buffer, size_t buffer_size);
  CWK_PUBLIC bool cwk_path_is_separator(const char* str);
  CWK_PUBLIC enum cwk_path_style cwk_path_guess_style(const char* path);
  CWK_PUBLIC void cwk_path_set_style(enum cwk_path_style style);
  CWK_PUBLIC enum cwk_path_style cwk_path_get_style(void);

#include <stdarg.h>
#include <stdio.h>
#include <string.h>

#if defined(WIN32) || defined(_WIN32) ||                                       \
  defined(__WIN32) && !defined(__CYGWIN__)
static enum cwk_path_style path_style = CWK_STYLE_WINDOWS;
#else
static enum cwk_path_style path_style = CWK_STYLE_UNIX;
#endif

static const char* separators[] = {
  "\\/"
  "/"  
};

struct cwk_segment_joined
{
  struct cwk_segment segment;
  const char** paths;
  size_t path_index;
};

static size_t cwk_path_output_sized(char* buffer, size_t buffer_size,
  size_t position, const char* str, size_t length)
{
  size_t amount_written;

  if (buffer_size > position + length) {
    amount_written = length;
  } else if (buffer_size > position) {
    amount_written = buffer_size - position;
  } else {
    amount_written = 0;
  }

  if (amount_written > 0) {
    memmove(&buffer[position], str, amount_written);
  }

  return length;
}

static size_t cwk_path_output_current(char* buffer, size_t buffer_size,
  size_t position)
{
  return cwk_path_output_sized(buffer, buffer_size, position, ".", 1);
}

static size_t cwk_path_output_back(char* buffer, size_t buffer_size,
  size_t position)
{
  return cwk_path_output_sized(buffer, buffer_size, position, "..", 2);
}

static size_t cwk_path_output_separator(char* buffer, size_t buffer_size,
  size_t position)
{
  return cwk_path_output_sized(buffer, buffer_size, position,
    separators[path_style], 1);
}

static size_t cwk_path_output_dot(char* buffer, size_t buffer_size,
  size_t position)
{
  return cwk_path_output_sized(buffer, buffer_size, position, ".", 1);
}

static size_t cwk_path_output(char* buffer, size_t buffer_size, size_t position,
  const char* str)
{
  size_t length;

  length = strlen(str);
  return cwk_path_output_sized(buffer, buffer_size, position, str, length);
}

static void cwk_path_terminate_output(char* buffer, size_t buffer_size,
  size_t pos)
{
  if (buffer_size > 0) {
    if (pos >= buffer_size) {
      buffer[buffer_size - 1] = '\0';
    } else {
      buffer[pos] = '\0';
    }
  }
}

static bool cwk_path_is_string_equal(const char* first, const char* second,
  size_t n)
{
  if (path_style == CWK_STYLE_UNIX) {
    return strncmp(first, second, n) == 0;
  }

  while (*first && *second && n > 0) {


    if (tolower(*first++) != tolower(*second++)) {
      return false;
    }

    --n;
  }

  return n == 0 || (*first == '\0' && *second == '\0');
}

static const char* cwk_path_find_next_stop(const char* c)
{
  while (*c != '\0' && !cwk_path_is_separator(c)) {
    ++c;
  }

  return c;
}

static const char* cwk_path_find_previous_stop(const char* begin, const char* c)
{
  while (c > begin && !cwk_path_is_separator(c)) {
    --c;
  }

  if (cwk_path_is_separator(c)) {
    return c + 1;
  } else {
    return c;
  }
}

static bool cwk_path_get_first_segment_without_root(const char* path,
  const char* segments, struct cwk_segment* segment)
{
  segment->path = path;
  segment->segments = segments;
  segment->begin = segments;
  segment->end = segments;
  segment->size = 0;

  if (*segments == '\0') {
    return false;
  }

  while (cwk_path_is_separator(segments)) {
    ++segments;
    if (*segments == '\0') {
      return false;
    }
  }

  segment->begin = segments;

  segments = cwk_path_find_next_stop(segments);

  segment->size = (size_t)(segments - segment->begin);
  segment->end = segments;

  return true;
}

static bool cwk_path_get_last_segment_without_root(const char* path,
  struct cwk_segment* segment)
{
  if (!cwk_path_get_first_segment_without_root(path, path, segment)) {
    return false;
  }

  while (cwk_path_get_next_segment(segment)) {

  }

  return true;
}

static bool cwk_path_get_first_segment_joined(const char** paths,
  struct cwk_segment_joined* sj)
{
  bool result;

  sj->path_index = 0;
  sj->paths = paths;

  result = false;
  while (paths[sj->path_index] != NULL &&
    (result = cwk_path_get_first_segment(paths[sj->path_index],
      &sj->segment)) == false) {
    ++sj->path_index;
  }

  return result;
}

static bool cwk_path_get_next_segment_joined(struct cwk_segment_joined* sj)
{
  bool result;

  if (sj->paths[sj->path_index] == NULL) {


    return false;
  } else if (cwk_path_get_next_segment(&sj->segment)) {


    return true;
  }

  result = false;

  do {
    ++sj->path_index;


    if (sj->paths[sj->path_index] == NULL) {
      break;
    }





    result = cwk_path_get_first_segment_without_root(sj->paths[sj->path_index],
      sj->paths[sj->path_index], &sj->segment);

  } while (!result);

  return result;
}

static bool cwk_path_get_previous_segment_joined(struct cwk_segment_joined* sj)
{
  bool result;

  if (*sj->paths == NULL) {



    return false;
  } else if (cwk_path_get_previous_segment(&sj->segment)) {


    return true;
  }

  result = false;

  do {


    if (sj->path_index == 0) {
      break;
    }



    --sj->path_index;



    if (sj->path_index == 0) {
      result = cwk_path_get_last_segment(sj->paths[sj->path_index],
        &sj->segment);
    } else {
      result = cwk_path_get_last_segment_without_root(sj->paths[sj->path_index],
        &sj->segment);
    }

  } while (!result);

  return result;
}

static bool cwk_path_segment_back_will_be_removed(struct cwk_segment_joined* sj)
{
  enum cwk_segment_type type;
  int counter;


  counter = 0;

  while (cwk_path_get_previous_segment_joined(sj)) {




    type = cwk_path_get_segment_type(&sj->segment);
    if (type == CWK_NORMAL) {
  
  
  
      ++counter;
      if (counter > 0) {
        return true;
      }
    } else if (type == CWK_BACK) {
  
  
  
      --counter;
    }
  }

  return false;
}

static bool cwk_path_segment_normal_will_be_removed(
  struct cwk_segment_joined* sj)
{
  enum cwk_segment_type type;
  int counter;

  counter = 0;

  while (cwk_path_get_next_segment_joined(sj)) {




    type = cwk_path_get_segment_type(&sj->segment);
    if (type == CWK_NORMAL) {
  
  
      ++counter;
    } else if (type == CWK_BACK) {
  
  
      --counter;
      if (counter < 0) {
        return true;
      }
    }
  }

  return false;
}

static bool
cwk_path_segment_will_be_removed(const struct cwk_segment_joined* sj,
  bool absolute)
{
  enum cwk_segment_type type;
  struct cwk_segment_joined sjc;

  sjc = *sj;

  type = cwk_path_get_segment_type(&sj->segment);
  if (type == CWK_CURRENT) {
    return true;
  } else if (type == CWK_BACK && absolute) {
    return true;
  } else if (type == CWK_BACK) {
    return cwk_path_segment_back_will_be_removed(&sjc);
  } else {
    return cwk_path_segment_normal_will_be_removed(&sjc);
  }
}

static bool
cwk_path_segment_joined_skip_invisible(struct cwk_segment_joined* sj,
  bool absolute)
{
  while (cwk_path_segment_will_be_removed(sj, absolute)) {
    if (!cwk_path_get_next_segment_joined(sj)) {
      return false;
    }
  }

  return true;
}

static void cwk_path_get_root_windows(const char* path, size_t* length)
{
  const char* c;
  bool is_device_path;

  c = path;
  *length = 0;
  if (!*c) {
    return;
  }

  if (cwk_path_is_separator(c)) {
    ++c;



    if (!cwk_path_is_separator(c)) {
  
  
      ++(*length);
      return;
    }








    ++c;
    is_device_path = (*c == '?' || *c == '.') && cwk_path_is_separator(++c);
    if (is_device_path) {
  
  
  
      *length = 4;
      return;
    }



    c = cwk_path_find_next_stop(c);



    while (cwk_path_is_separator(c)) {
      ++c;
    }



    c = cwk_path_find_next_stop(c);



    if (cwk_path_is_separator(c)) {
      ++c;
    }


    *length = (size_t)(c - path);
    return;
  }

  if (*++c == ':') {
    *length = 2;





    if (cwk_path_is_separator(++c)) {
      *length = 3;
    }
  }
}

static void cwk_path_get_root_unix(const char* path, size_t* length)
{
  if (cwk_path_is_separator(path)) {
    *length = 1;
  } else {
    *length = 0;
  }
}

static bool cwk_path_is_root_absolute(const char* path, size_t length)
{
  if (length == 0) {
    return false;
  }

  return cwk_path_is_separator(&path[length - 1]);
}

static size_t cwk_path_join_and_normalize_multiple(const char** paths,
  char* buffer, size_t buffer_size)
{
  size_t pos;
  bool absolute, has_segment_output;
  struct cwk_segment_joined sj;

  cwk_path_get_root(paths[0], &pos);

  absolute = cwk_path_is_root_absolute(paths[0], pos);

  cwk_path_output_sized(buffer, buffer_size, 0, paths[0], pos);

  if (!cwk_path_get_first_segment_joined(paths, &sj)) {
    goto done;
  }

  has_segment_output = false;

  do {


    if (cwk_path_segment_will_be_removed(&sj, absolute)) {
      continue;
    }





    if (has_segment_output) {
      pos += cwk_path_output_separator(buffer, buffer_size, pos);
    }




    has_segment_output = true;




    pos += cwk_path_output_sized(buffer, buffer_size, pos, sj.segment.begin,
      sj.segment.size);
  } while (cwk_path_get_next_segment_joined(&sj));

  if (!has_segment_output && pos == 0) {



    assert(absolute == false);
    pos += cwk_path_output_current(buffer, buffer_size, pos);
  }

done:
  cwk_path_terminate_output(buffer, buffer_size, pos);

  return pos;
}

size_t cwk_path_get_absolute(const char* base, const char* path, char* buffer,
  size_t buffer_size)
{
  size_t i;
  const char* paths[4];

  if (cwk_path_is_absolute(base)) {
    i = 0;
  } else if (path_style == CWK_STYLE_WINDOWS) {
    paths[0] = "\\";
    i = 1;
  } else {
    paths[0] = "/";
    i = 1;
  }

  if (cwk_path_is_absolute(path)) {


    paths[i++] = path;
    paths[i] = NULL;
  } else {


    paths[i++] = base;
    paths[i++] = path;
    paths[i] = NULL;
  }

  return cwk_path_join_and_normalize_multiple(paths, buffer, buffer_size);
}

static void cwk_path_skip_segments_until_diverge(struct cwk_segment_joined* bsj,
  struct cwk_segment_joined* osj, bool absolute, bool* base_available,
  bool* other_available)
{
  do {




    *base_available = cwk_path_segment_joined_skip_invisible(bsj, absolute);
    *other_available = cwk_path_segment_joined_skip_invisible(osj, absolute);




    if (!*base_available || !*other_available) {
      break;
    }



    if (!cwk_path_is_string_equal(bsj->segment.begin, osj->segment.begin,
      bsj->segment.size)) {
      break;
    }




    *base_available = cwk_path_get_next_segment_joined(bsj);
    *other_available = cwk_path_get_next_segment_joined(osj);
  } while (*base_available && *other_available);
}

size_t cwk_path_get_relative(const char* base_directory, const char* path,
  char* buffer, size_t buffer_size)
{
  size_t pos, base_root_length, path_root_length;
  bool absolute, base_available, other_available, has_output;
  const char* base_paths[2], * other_paths[2];
  struct cwk_segment_joined bsj, osj;

  pos = 0;

  cwk_path_get_root(base_directory, &base_root_length);
  cwk_path_get_root(path, &path_root_length);
  if (base_root_length != path_root_length ||
    !cwk_path_is_string_equal(base_directory, path, base_root_length)) {
    cwk_path_terminate_output(buffer, buffer_size, pos);
    return pos;
  }

  absolute = cwk_path_is_root_absolute(base_directory, base_root_length);

  base_paths[0] = base_directory;
  base_paths[1] = NULL;
  other_paths[0] = path;
  other_paths[1] = NULL;
  cwk_path_get_first_segment_joined(base_paths, &bsj);
  cwk_path_get_first_segment_joined(other_paths, &osj);

  cwk_path_skip_segments_until_diverge(&bsj, &osj, absolute, &base_available,
    &other_available);

  has_output = false;

  if (base_available) {
    do {
  
  
      if (!cwk_path_segment_joined_skip_invisible(&bsj, absolute)) {
        break;
      }

  
  
      has_output = true;

  
  
      pos += cwk_path_output_back(buffer, buffer_size, pos);
      pos += cwk_path_output_separator(buffer, buffer_size, pos);
    } while (cwk_path_get_next_segment_joined(&bsj));
  }

  if (other_available) {
    do {
  
  
      if (!cwk_path_segment_joined_skip_invisible(&osj, absolute)) {
        break;
      }

  
  
      has_output = true;

  
  
      pos += cwk_path_output_sized(buffer, buffer_size, pos, osj.segment.begin,
        osj.segment.size);
      pos += cwk_path_output_separator(buffer, buffer_size, pos);
    } while (cwk_path_get_next_segment_joined(&osj));
  }

  if (has_output) {
    --pos;
  } else {
    pos += cwk_path_output_current(buffer, buffer_size, pos);
  }

  cwk_path_terminate_output(buffer, buffer_size, pos);

  return pos;
}

size_t cwk_path_join(const char* path_a, const char* path_b, char* buffer,
  size_t buffer_size)
{
  const char* paths[3];

  paths[0] = path_a;
  paths[1] = path_b;
  paths[2] = NULL;

  return cwk_path_join_and_normalize_multiple(paths, buffer, buffer_size);
}

size_t cwk_path_join_multiple(const char** paths, char* buffer,
  size_t buffer_size)
{
  return cwk_path_join_and_normalize_multiple(paths, buffer, buffer_size);
}

void cwk_path_get_root(const char* path, size_t* length)
{
  if (path_style == CWK_STYLE_WINDOWS) {
    cwk_path_get_root_windows(path, length);
  } else {
    cwk_path_get_root_unix(path, length);
  }
}

size_t cwk_path_change_root(const char* path, const char* new_root,
  char* buffer, size_t buffer_size)
{
  const char* tail;
  size_t root_length, path_length, tail_length, new_root_length, new_path_size;

  cwk_path_get_root(path, &root_length);

  new_root_length = strlen(new_root);
  path_length = strlen(path);

  tail = path + root_length;
  tail_length = path_length - root_length;

  cwk_path_output_sized(buffer, buffer_size, new_root_length, tail,
    tail_length);
  cwk_path_output_sized(buffer, buffer_size, 0, new_root, new_root_length);

  new_path_size = tail_length + new_root_length;
  cwk_path_terminate_output(buffer, buffer_size, new_path_size);

  return new_path_size;
}

bool cwk_path_is_absolute(const char* path)
{
  size_t length;

  cwk_path_get_root(path, &length);

  return cwk_path_is_root_absolute(path, length);
}

bool cwk_path_is_relative(const char* path)
{
  return !cwk_path_is_absolute(path);
}

void cwk_path_get_basename(const char* path, const char** basename,
  size_t* length)
{
  struct cwk_segment segment;

  if (!cwk_path_get_last_segment(path, &segment)) {
    *basename = NULL;
    *length = 0;
    return;
  }

  *basename = segment.begin;
  *length = segment.size;
}

size_t cwk_path_change_basename(const char* path, const char* new_basename,
  char* buffer, size_t buffer_size)
{
  struct cwk_segment segment;
  size_t pos, root_size, new_basename_size;

  if (!cwk_path_get_last_segment(path, &segment)) {



    cwk_path_get_root(path, &root_size);
    pos = cwk_path_output_sized(buffer, buffer_size, 0, path, root_size);



    while (cwk_path_is_separator(new_basename)) {
      ++new_basename;
    }



    new_basename_size = 0;
    while (new_basename[new_basename_size]) {
      ++new_basename_size;
    }



    while (new_basename_size > 0 &&
      cwk_path_is_separator(&new_basename[new_basename_size - 1])) {
      --new_basename_size;
    }


    pos += cwk_path_output_sized(buffer, buffer_size, pos, new_basename,
      new_basename_size);


    cwk_path_terminate_output(buffer, buffer_size, pos);
    return pos;
  }

  return cwk_path_change_segment(&segment, new_basename, buffer, buffer_size);
}

void cwk_path_get_dirname(const char* path, size_t* length)
{
  struct cwk_segment segment;

  if (!cwk_path_get_last_segment(path, &segment)) {
    *length = 0;
    return;
  }

  *length = (size_t)(segment.begin - path);
}

bool cwk_path_get_extension(const char* path, const char** extension,
  size_t* length)
{
  struct cwk_segment segment;
  const char* c;

  if (!cwk_path_get_last_segment(path, &segment)) {
    return false;
  }

  for (c = segment.end; c >= segment.begin; --c) {
    if (*c == '.') {
  
      *extension = c;
      *length = (size_t)(segment.end - c);
      return true;
    }
  }

  return false;
}

bool cwk_path_has_extension(const char* path)
{
  const char* extension;
  size_t length;

  return cwk_path_get_extension(path, &extension, &length);
}

size_t cwk_path_change_extension(const char* path, const char* new_extension,
  char* buffer, size_t buffer_size)
{
  struct cwk_segment segment;
  const char* c, * old_extension;
  size_t pos, root_size, trail_size, new_extension_size;

  if (!cwk_path_get_last_segment(path, &segment)) {




    cwk_path_get_root(path, &root_size);
    pos = cwk_path_output_sized(buffer, buffer_size, 0, path, root_size);


    if (*new_extension != '.') {
      pos += cwk_path_output_dot(buffer, buffer_size, pos);
    }


    pos += cwk_path_output(buffer, buffer_size, pos, new_extension);
    cwk_path_terminate_output(buffer, buffer_size, pos);
    return pos;
  }

  old_extension = segment.end;
  for (c = segment.begin; c < segment.end; ++c) {
    if (*c == '.') {
      old_extension = c;
    }
  }

  pos = cwk_path_output_sized(buffer, buffer_size, 0, segment.path,
    (size_t)(old_extension - segment.path));

  if (*new_extension == '.') {
    ++new_extension;
  }

  new_extension_size = strlen(new_extension) + 1;
  trail_size = cwk_path_output(buffer, buffer_size, pos + new_extension_size,
    segment.end);

  pos += cwk_path_output_dot(buffer, buffer_size, pos);
  pos += cwk_path_output(buffer, buffer_size, pos, new_extension);

  pos += trail_size;
  cwk_path_terminate_output(buffer, buffer_size, pos);

  return pos;
}

size_t cwk_path_normalize(const char* path, char* buffer, size_t buffer_size)
{
  const char* paths[2];

  paths[0] = path;
  paths[1] = NULL;

  return cwk_path_join_and_normalize_multiple(paths, buffer, buffer_size);
}

size_t cwk_path_get_intersection(const char* path_base, const char* path_other)
{
  bool absolute;
  size_t base_root_length, other_root_length;
  const char* end;
  const char* paths_base[2], * paths_other[2];
  struct cwk_segment_joined base, other;

  cwk_path_get_root(path_base, &base_root_length);
  cwk_path_get_root(path_other, &other_root_length);
  if (!cwk_path_is_string_equal(path_base, path_other, base_root_length)) {
    return 0;
  }

  paths_base[0] = path_base;
  paths_base[1] = NULL;
  paths_other[0] = path_other;
  paths_other[1] = NULL;

  if (!cwk_path_get_first_segment_joined(paths_base, &base) ||
    !cwk_path_get_first_segment_joined(paths_other, &other)) {
    return base_root_length;
  }

  absolute = cwk_path_is_root_absolute(path_base, base_root_length);

  end = path_base + base_root_length;

  do {


    if (!cwk_path_segment_joined_skip_invisible(&base, absolute) ||
      !cwk_path_segment_joined_skip_invisible(&other, absolute)) {
      break;
    }

    if (!cwk_path_is_string_equal(base.segment.begin, other.segment.begin,
      base.segment.size)) {
  
  
      return (size_t)(end - path_base);
    }


    end = base.segment.end;
  } while (cwk_path_get_next_segment_joined(&base) &&
    cwk_path_get_next_segment_joined(&other));

  return (size_t)(end - path_base);
}

bool cwk_path_get_first_segment(const char* path, struct cwk_segment* segment)
{
  size_t length;
  const char* segments;

  cwk_path_get_root(path, &length);
  segments = path + length;

  return cwk_path_get_first_segment_without_root(path, segments, segment);
}

bool cwk_path_get_last_segment(const char* path, struct cwk_segment* segment)
{
  if (!cwk_path_get_first_segment(path, segment)) {
    return false;
  }

  while (cwk_path_get_next_segment(segment)) {

  }

  return true;
}

bool cwk_path_get_next_segment(struct cwk_segment* segment)
{
  const char* c;

  c = segment->begin + segment->size;
  if (*c == '\0') {
    return false;
  }

  assert(cwk_path_is_separator(c));
  do {
    ++c;
  } while (cwk_path_is_separator(c));

  if (*c == '\0') {
    return false;
  }

  segment->begin = c;

  c = cwk_path_find_next_stop(c);
  segment->end = c;
  segment->size = (size_t)(c - segment->begin);

  return true;
}

bool cwk_path_get_previous_segment(struct cwk_segment* segment)
{
  const char* c;
  c = segment->begin;
  if (c <= segment->segments) {
    return false;
  }
  do {
    --c;
    if (c < segment->segments) {
  
  
      return false;
    }
  } while (cwk_path_is_separator(c));
  segment->end = c + 1;
  segment->begin = cwk_path_find_previous_stop(segment->segments, c);
  segment->size = (size_t)(segment->end - segment->begin);
  return true;
}
enum cwk_segment_type cwk_path_get_segment_type(
  const struct cwk_segment* segment)
{
  if (strncmp(segment->begin, ".", segment->size) == 0) {
    return CWK_CURRENT;
  } else if (strncmp(segment->begin, "..", segment->size) == 0) {
    return CWK_BACK;
  }

  return CWK_NORMAL;
}
bool cwk_path_is_separator(const char* str)
{
  const char* c;
  c = separators[path_style];
  while (*c) {
    if (*c == *str) {
      return true;
    }
    ++c;
  }
  return false;
}
size_t cwk_path_change_segment(struct cwk_segment* segment, const char* value,
  char* buffer, size_t buffer_size)
{
  size_t pos, value_size, tail_size;
  pos = cwk_path_output_sized(buffer, buffer_size, 0, segment->path,
    (size_t)(segment->begin - segment->path));
  while (cwk_path_is_separator(value)) {
    ++value;
  }
  value_size = 0;
  while (value[value_size]) {
    ++value_size;
  }
  while (value_size > 0 && cwk_path_is_separator(&value[value_size - 1])) {
    --value_size;
  }
  tail_size = strlen(segment->end);
  cwk_path_output_sized(buffer, buffer_size, pos + value_size, segment->end,
    tail_size);
  pos += cwk_path_output_sized(buffer, buffer_size, pos, value, value_size);
  pos += tail_size;
  cwk_path_terminate_output(buffer, buffer_size, pos);
  return pos;
}
enum cwk_path_style cwk_path_guess_style(const char* path)
{
  const char* c;
  size_t root_length;
  struct cwk_segment segment;
  cwk_path_get_root_windows(path, &root_length);
  if (root_length > 1) {
    return CWK_STYLE_WINDOWS;
  }
  for (c = path; *c; ++c) {
    if (*c == *separators[CWK_STYLE_UNIX]) {
      return CWK_STYLE_UNIX;
    } else if (*c == *separators[CWK_STYLE_WINDOWS]) {
      return CWK_STYLE_WINDOWS;
    }
  }
  if (!cwk_path_get_last_segment(path, &segment)) {
    return CWK_STYLE_UNIX;
  }
  if (*segment.begin == '.') {
    return CWK_STYLE_UNIX;
  }
  for (c = segment.begin; *c; ++c) {
    if (*c == '.') {
      return CWK_STYLE_WINDOWS;
    }
  }
  return CWK_STYLE_UNIX;
}
void cwk_path_set_style(enum cwk_path_style style)
{
  assert(style == CWK_STYLE_UNIX || style == CWK_STYLE_WINDOWS);
  path_style = style;
}
enum cwk_path_style cwk_path_get_style(void)
{
  return path_style;
}
}