/**___________________________________________________________________________
 *
 * Pyomo: Python Optimization Modeling Objects
 * Copyright (c) 2008-2025
 * National Technology and Engineering Solutions of Sandia, LLC
 * Under the terms of Contract DE-NA0003525 with National Technology and
 * Engineering Solutions of Sandia, LLC, the U.S. Government retains certain
 * rights in this software.
 * This software is distributed under the 3-clause BSD License.
 * ___________________________________________________________________________
**/

#include "model_base.hpp"

bool constraint_sorter(std::shared_ptr<Constraint> c1,
                       std::shared_ptr<Constraint> c2) {
  return c1->index < c2->index;
}

Model::Model() {
  constraints =
      std::set<std::shared_ptr<Constraint>, decltype(constraint_sorter) *>(
          constraint_sorter);
}

void Model::add_constraint(std::shared_ptr<Constraint> con) {
  con->index = current_con_ndx;
  current_con_ndx += 1;
  constraints.insert(constraints.end(), con);
}

void Model::remove_constraint(std::shared_ptr<Constraint> con) {
  constraints.erase(con);
  con->index = -1;
}
