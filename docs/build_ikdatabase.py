# -*- coding: utf-8 -*-
# Copyright (C) 2011 Rosen Diankov (rosen.diankov@gmail.com)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from openravepy import *
from numpy import *
from optparse import OptionParser
import os
import scipy

def build(stats,options,outputdir):
    mkdir_recursive(outputdir)
    iktypes = ', '.join(iktype.name for iktype in IkParameterization.Type.values.values())
    text="""
.. _ikfast-database:

--------------------------------------------------------
IKFast v%s Database
========================

A collection for robots and statistics for the compiled inverse kinematics files using :mod:`IKFast <ikfast>`. This database is automatically generated by the `OpenRAVE Testing Server`_. All possible IKs for each robot's manipulator are generated. The database provides URL links to the robot files, genreated ik files, and test results history.

.. toctree::
  :maxdepth: 1
  
  testing

* :ref:`Supported inverse kinematics types <ikfast_types>`

The following results originate from `this run <%s>`_.

"""%(ikfast.__version__,options.jenkinsbuild_url)
    open(os.path.join(outputdir,'index.rst'),'w').write(text)

    freeparameters = ', '.join('%s free - %s tests'%(i,num) for i,num in enumerate(options.numiktests))
    testing_text="""
.. _ikfast-testing:

IKFast Performance Testing
==========================

There are four different ways of calling the IK solver:

* GetSolution(*goal*) - call with just the end effector parameterization, return the first solution found within limits.
* GetSolution(*goal*,*free*) - call with end effector parameterization and specify all free joint values, return the first solution found within limits.
* GetSolutions(*goal*) - call with just the end effector parameterization, return all solutions searching through all free joint values.
* GetSolutions(*goal*,*free*) - call with end effector parameterization and specify all free joint values, return all possible solutions.

The following algorithm tests these four calls by:

1. Randomly sample a robot configuration and compute the correct parameterization of the end effector *goal* and free joint values *free*.
2. Move the robot to a random position.
3. Call GetSolution(*goal*), GetSolutions(*goal*), GetSolutions(*goal*,*free*)
4. Call GetSolution(*goal*,*free_random*) and GetSolutions(*goal*,*free_random*). Check that the returned solutions have same values as free parameters.

For every end effector parameterization and a returned solution, set the returned solution on the robot and compute the error between the original end effector and the new end effector. If the error is *greater than %f*, then the IK is wrong and the iteration is a *failure*. If no wrong solutions were returned and at least one correct IK solution is found within limits, then the iteration is a *success*. When the free values are not specified, the IK solver will discretize the range of the freevalues and test with all possible combinations [1]_. 

The number of tests is determined by the number of free parameters: %s

Four values are extracted to measure the performance of a generated IK solver:

* wrong rate - number of parameterizations where at least one wrong solution was returned.
* success rate - number of parameterizations where all returned solutions are correct
* no solution rate - number of parameterizations where no solutions were found within limits
* missing solution rate - number of parameterizations where the specific sampled solution was not returned, but at least one solution was found.

An IK is **successful** if the wrong rate is 0, success rate is > %f, and the no solution rate is < %f. 
The raw function call run-time is also recorded.

Degenerate configurations can frequently occur when the robot axes align, this produces a lot of divide by zero conditions inside the IK. In order to check all such code paths, the configuration sampler common tests angles 0, pi/2, pi, and -pi/2.

.. [1] The discretization of the free joint values depends on the robot manipulator and is given in each individual manipulator page.
"""%(options.errorthreshold,freeparameters,options.minimumsuccess,options.maximumnosolutions)
    open(os.path.join(outputdir,'testing.rst'),'w').write(testing_text)

if __name__ == "__main__":
    stats,options = pickle.load(open('ikfaststats.pp','r'))
    build(stats,options,'en/ikfast')
