/*
 * This program is free software; you can redistribute it and/or
 * modify it under the terms of the GNU General Public License
 * as published by the Free Software Foundation; either version 2
 * of the License, or (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program; if not, write to the Free Software Foundation,
 * Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
 */

#pragma once

#include "FN_cpp_type.hh"

#include "BKE_attribute.h"
#include "BKE_geometry_set.hh"

struct Mesh;

namespace blender::bke {

using fn::CPPType;

class ReadAttribute {
 protected:
  const AttributeDomain domain_;
  const CPPType &cpp_type_;
  const int64_t size_;

 public:
  ReadAttribute(AttributeDomain domain, const CPPType &cpp_type, const int64_t size)
      : domain_(domain), cpp_type_(cpp_type), size_(size)
  {
  }

  virtual ~ReadAttribute() = default;

  AttributeDomain domain() const
  {
    return domain_;
  }

  const CPPType &cpp_type() const
  {
    return cpp_type_;
  }

  int64_t size() const
  {
    return size_;
  }

  void get(const int64_t index, void *r_value) const
  {
    BLI_assert(index < size_);
    this->get_internal(index, r_value);
  }

  template<typename T> T get(const int64_t index) const
  {
    BLI_assert(index < size_);
    T value;
    value.~T();
    this->get_internal(index, &value);
    return value;
  }

 protected:
  /* r_value is expected to be uninitialized. */
  virtual void get_internal(const int64_t index, void *r_value) const = 0;
};

using ReadAttributePtr = std::unique_ptr<ReadAttribute>;

ReadAttributePtr mesh_attribute_get_for_read(const MeshComponent &mesh_component,
                                             const StringRef attribute_name);

ReadAttributePtr mesh_attribute_adapt_domain(const MeshComponent &mesh_component,
                                             ReadAttributePtr attribute,
                                             const AttributeDomain to_domain);

ReadAttributePtr mesh_attribute_get_for_read(const MeshComponent &mesh_component,
                                             const StringRef attribute_name,
                                             const AttributeDomain domain,
                                             const CPPType &cpp_type,
                                             const void *default_value = nullptr);

}  // namespace blender::bke