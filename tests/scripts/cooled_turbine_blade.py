# Copyright (C) 2023 - 2024 ANSYS, Inc. and/or its affiliates.
# SPDX-License-Identifier: MIT
#
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

""" .. _ref_example_02_td_006:

Thermal-Stress Analysis of a Cooled Turbine Blade
-------------------------------------------------

Unit System: MKS.

Coverage:
3D Thermal-Stress Analysis of a Cooled Turbine Blade.
Convection, Mass Flow Rate, Temperatures are applied
to Thermal Fluid bodies. Adiabatic surfaces are fixed.
Solved Thermal Stress analysis.

Validation:
Validated Solid Region Temperature Distribution,
Fluid Temperatures, Solid Surface Temperatures,
Fluid Temperature Along Path of Hole Number 1,
Solid Temperature Along Path of Hole Number 1.
Validated maximum Von Mises Stresses for Solid Region,
Von Mises Stress Along Path of Hole Number 1.

"""
import os
import os.path
import string
import json

from Ansys.ACT.Automation import Mechanical

# Define python variables
ExtAPI.Application.ActiveUnitSystem = MechanicalUnitSystem.StandardMKS
ExtAPI.Application.ActiveMetricTemperatureUnit = MetricTemperatureUnitType.Kelvin

GEOM = Model.Geometry
CS_GRP = Model.CoordinateSystems
MSH = Model.Mesh
STAT_THERM = ExtAPI.DataModel.AnalysisByName("Steady-State Thermal")
STAT_THERM_SOLN = STAT_THERM.Solution
STAT_STRUC = ExtAPI.DataModel.AnalysisByName("Static Structural")
STAT_STRUC_SOLN = STAT_STRUC.Solution

NS_Passage1 = [x for x in Model.GetChildren[Ansys.ACT.Automation.Mechanical.NamedSelection](True) if x.Name == 'Passage 1'][0]
NS_Passage2 = [x for x in Model.GetChildren[Ansys.ACT.Automation.Mechanical.NamedSelection](True) if x.Name == 'Passage 2'][0]
NS_Passage3 = [x for x in Model.GetChildren[Ansys.ACT.Automation.Mechanical.NamedSelection](True) if x.Name == 'Passage 3'][0]
NS_Passage4 = [x for x in Model.GetChildren[Ansys.ACT.Automation.Mechanical.NamedSelection](True) if x.Name == 'Passage 4'][0]
NS_Passage5 = [x for x in Model.GetChildren[Ansys.ACT.Automation.Mechanical.NamedSelection](True) if x.Name == 'Passage 5'][0]
NS_Passage6 = [x for x in Model.GetChildren[Ansys.ACT.Automation.Mechanical.NamedSelection](True) if x.Name == 'Passage 6'][0]
NS_Passage7 = [x for x in Model.GetChildren[Ansys.ACT.Automation.Mechanical.NamedSelection](True) if x.Name == 'Passage 7'][0]
NS_Passage8 = [x for x in Model.GetChildren[Ansys.ACT.Automation.Mechanical.NamedSelection](True) if x.Name == 'Passage 8'][0]
NS_Passage9 = [x for x in Model.GetChildren[Ansys.ACT.Automation.Mechanical.NamedSelection](True) if x.Name == 'Passage 9'][0]
NS_Passage10 = [x for x in Model.GetChildren[Ansys.ACT.Automation.Mechanical.NamedSelection](True) if x.Name == 'Passage 10'][0]
NS_Hole1 = [x for x in Model.GetChildren[Ansys.ACT.Automation.Mechanical.NamedSelection](True) if x.Name == 'Hole 1'][0]
NS_Hole2 = [x for x in Model.GetChildren[Ansys.ACT.Automation.Mechanical.NamedSelection](True) if x.Name == 'Hole 2'][0]
NS_Hole3 = [x for x in Model.GetChildren[Ansys.ACT.Automation.Mechanical.NamedSelection](True) if x.Name == 'Hole 3'][0]
NS_Hole4 = [x for x in Model.GetChildren[Ansys.ACT.Automation.Mechanical.NamedSelection](True) if x.Name == 'Hole 4'][0]
NS_Hole5 = [x for x in Model.GetChildren[Ansys.ACT.Automation.Mechanical.NamedSelection](True) if x.Name == 'Hole 5'][0]
NS_Hole6 = [x for x in Model.GetChildren[Ansys.ACT.Automation.Mechanical.NamedSelection](True) if x.Name == 'Hole 6'][0]
NS_Hole7 = [x for x in Model.GetChildren[Ansys.ACT.Automation.Mechanical.NamedSelection](True) if x.Name == 'Hole 7'][0]
NS_Hole8 = [x for x in Model.GetChildren[Ansys.ACT.Automation.Mechanical.NamedSelection](True) if x.Name == 'Hole 8'][0]
NS_Hole9 = [x for x in Model.GetChildren[Ansys.ACT.Automation.Mechanical.NamedSelection](True) if x.Name == 'Hole 9'][0]
NS_Hole10 = [x for x in Model.GetChildren[Ansys.ACT.Automation.Mechanical.NamedSelection](True) if x.Name == 'Hole 10'][0]
NS_Inlet1 = [x for x in Model.GetChildren[Ansys.ACT.Automation.Mechanical.NamedSelection](True) if x.Name == 'Inlet 1'][0]
NS_Inlet2 = [x for x in Model.GetChildren[Ansys.ACT.Automation.Mechanical.NamedSelection](True) if x.Name == 'Inlet 2'][0]
NS_Inlet3 = [x for x in Model.GetChildren[Ansys.ACT.Automation.Mechanical.NamedSelection](True) if x.Name == 'Inlet 3'][0]
NS_Inlet4 = [x for x in Model.GetChildren[Ansys.ACT.Automation.Mechanical.NamedSelection](True) if x.Name == 'Inlet 4'][0]
NS_Inlet5 = [x for x in Model.GetChildren[Ansys.ACT.Automation.Mechanical.NamedSelection](True) if x.Name == 'Inlet 5'][0]
NS_Inlet6 = [x for x in Model.GetChildren[Ansys.ACT.Automation.Mechanical.NamedSelection](True) if x.Name == 'Inlet 6'][0]
NS_Inlet7 = [x for x in Model.GetChildren[Ansys.ACT.Automation.Mechanical.NamedSelection](True) if x.Name == 'Inlet 7'][0]
NS_Inlet8 = [x for x in Model.GetChildren[Ansys.ACT.Automation.Mechanical.NamedSelection](True) if x.Name == 'Inlet 8'][0]
NS_Inlet9 = [x for x in Model.GetChildren[Ansys.ACT.Automation.Mechanical.NamedSelection](True) if x.Name == 'Inlet 9'][0]
NS_Inlet10 = [x for x in Model.GetChildren[Ansys.ACT.Automation.Mechanical.NamedSelection](True) if x.Name == 'Inlet 10'][0]
NS_Path1 = [x for x in Model.GetChildren[Ansys.ACT.Automation.Mechanical.NamedSelection](True) if x.Name == 'Path1'][0]
NS_Path2 = [x for x in Model.GetChildren[Ansys.ACT.Automation.Mechanical.NamedSelection](True) if x.Name == 'Path2'][0]
NS_Faces4 = [x for x in Model.GetChildren[Ansys.ACT.Automation.Mechanical.NamedSelection](True) if x.Name == 'Faces4'][0]
NS_Face1 = [x for x in Model.GetChildren[Ansys.ACT.Automation.Mechanical.NamedSelection](True) if x.Name == 'Face1'][0]
NS_Face2 = [x for x in Model.GetChildren[Ansys.ACT.Automation.Mechanical.NamedSelection](True) if x.Name == 'Face2'][0]
NS_Body1 = [x for x in Model.GetChildren[Ansys.ACT.Automation.Mechanical.NamedSelection](True) if x.Name == 'Body1'][0]
NS_Bodies10 = [x for x in Model.GetChildren[Ansys.ACT.Automation.Mechanical.NamedSelection](True) if x.Name == 'Bodies10'][0]

# Assign materials to blade and fluid bodies and model type for line bodies
GEOM.Children[0].Material = 'Blade'
for i in range(1,11):
	GEOM.Children[i].Material = 'Fluid'
	GEOM.Children[i].Children[0].ModelType = PrototypeModelType.ModelPhysicsTypeFluid
	GEOM.Children[i].Children[0].FluidDiscretization = FluidDiscretizationType.FluidUpwindExponential

# Define coordinate systems and paths
LCS01 = CS_GRP.AddCoordinateSystem()
LCS01.OriginLocation = NS_Path1

LCS02 = CS_GRP.AddCoordinateSystem()
LCS02.OriginLocation = NS_Path2

CONST_GEOM = Model.AddConstructionGeometry()
PATH01 = CONST_GEOM.AddPath()
PATH01.PathType = PathScopingType.Edge
PATH01.Location = NS_Passage1

PATH02 = CONST_GEOM.AddPath()
PATH02.PathType = PathScopingType.Points
PATH02.StartCoordinateSystem = LCS01
PATH02.EndCoordinateSystem = LCS02

# Setup loads and supports in linked steady-state thermal and static structural analyses
CONV01 = STAT_THERM.AddConvection()
CONV01.Location = NS_Hole1
CONV01.FilmCoefficient.Output.DiscreteValues = [Quantity('295430 [W m^-1 m^-1 K^-1]')]
CONV01.HasFluidFlow = True
CONV01.FluidFlowSelection = NS_Passage1

CONV02 = STAT_THERM.AddConvection()
CONV02.Location = NS_Hole2
CONV02.FilmCoefficient.Output.DiscreteValues = [Quantity('296290 [W m^-1 m^-1 K^-1]')]
CONV02.HasFluidFlow = True
CONV02.FluidFlowSelection = NS_Passage2

CONV03 = STAT_THERM.AddConvection()
CONV03.Location = NS_Hole3
CONV03.FilmCoefficient.Output.DiscreteValues = [Quantity('300760 [W m^-1 m^-1 K^-1]')]
CONV03.HasFluidFlow = True
CONV03.FluidFlowSelection = NS_Passage3

CONV04 = STAT_THERM.AddConvection()
CONV04.Location = NS_Hole4
CONV04.FilmCoefficient.Output.DiscreteValues = [Quantity('314160 [W m^-1 m^-1 K^-1]')]
CONV04.HasFluidFlow = True
CONV04.FluidFlowSelection = NS_Passage4

CONV05 = STAT_THERM.AddConvection()
CONV05.Location = NS_Hole5
CONV05.FilmCoefficient.Output.DiscreteValues = [Quantity('314950 [W m^-1 m^-1 K^-1]')]
CONV05.HasFluidFlow = True
CONV05.FluidFlowSelection = NS_Passage5

CONV06 = STAT_THERM.AddConvection()
CONV06.Location = NS_Hole6
CONV06.FilmCoefficient.Output.DiscreteValues = [Quantity('301990 [W m^-1 m^-1 K^-1]')]
CONV06.HasFluidFlow = True
CONV06.FluidFlowSelection = NS_Passage6

CONV07 = STAT_THERM.AddConvection()
CONV07.Location = NS_Hole7
CONV07.FilmCoefficient.Output.DiscreteValues = [Quantity('302470 [W m^-1 m^-1 K^-1]')]
CONV07.HasFluidFlow = True
CONV07.FluidFlowSelection = NS_Passage7

CONV08 = STAT_THERM.AddConvection()
CONV08.Location = NS_Hole8
CONV08.FilmCoefficient.Output.DiscreteValues = [Quantity('443430 [W m^-1 m^-1 K^-1]')]
CONV08.HasFluidFlow = True
CONV08.FluidFlowSelection = NS_Passage8

CONV09 = STAT_THERM.AddConvection()
CONV09.Location = NS_Hole9
CONV09.FilmCoefficient.Output.DiscreteValues = [Quantity('285270 [W m^-1 m^-1 K^-1]')]
CONV09.HasFluidFlow = True
CONV09.FluidFlowSelection = NS_Passage9

CONV010 = STAT_THERM.AddConvection()
CONV010.Location = NS_Hole10
CONV010.FilmCoefficient.Output.DiscreteValues = [Quantity('895860 [W m^-1 m^-1 K^-1]')]
CONV010.HasFluidFlow = True
CONV010.FluidFlowSelection = NS_Passage10

MFLOW_RT01 = STAT_THERM.AddMassFlowRate()
MFLOW_RT01.Location = NS_Passage1
MFLOW_RT01.Magnitude.Output.DiscreteValues = [Quantity('0[kg sec^-1]'), Quantity('-0.0228[kg sec^-1]')]

MFLOW_RT02 = STAT_THERM.AddMassFlowRate()
MFLOW_RT02.Location = NS_Passage2
MFLOW_RT02.Magnitude.Output.DiscreteValues = [Quantity('0[kg sec^-1]'), Quantity('-0.0239[kg sec^-1]')]

MFLOW_RT03 = STAT_THERM.AddMassFlowRate()
MFLOW_RT03.Location = NS_Passage3
MFLOW_RT03.Magnitude.Output.DiscreteValues = [Quantity('0[kg sec^-1]'), Quantity('-0.0228[kg sec^-1]')]

MFLOW_RT04 = STAT_THERM.AddMassFlowRate()
MFLOW_RT04.Location = NS_Passage4
MFLOW_RT04.Magnitude.Output.DiscreteValues = [Quantity('0[kg sec^-1]'), Quantity('-0.0243[kg sec^-1]')]

MFLOW_RT05 = STAT_THERM.AddMassFlowRate()
MFLOW_RT05.Location = NS_Passage5
MFLOW_RT05.Magnitude.Output.DiscreteValues = [Quantity('0[kg sec^-1]'), Quantity('-0.0239[kg sec^-1]')]

MFLOW_RT06 = STAT_THERM.AddMassFlowRate()
MFLOW_RT06.Location = NS_Passage6
MFLOW_RT06.Magnitude.Output.DiscreteValues = [Quantity('0[kg sec^-1]'), Quantity('-0.0242[kg sec^-1]')]

MFLOW_RT07 = STAT_THERM.AddMassFlowRate()
MFLOW_RT07.Location = NS_Passage7
MFLOW_RT07.Magnitude.Output.DiscreteValues = [Quantity('0[kg sec^-1]'), Quantity('-0.0232[kg sec^-1]')]

MFLOW_RT08 = STAT_THERM.AddMassFlowRate()
MFLOW_RT08.Location = NS_Passage8
MFLOW_RT08.Magnitude.Output.DiscreteValues = [Quantity('0[kg sec^-1]'), Quantity('-0.00799[kg sec^-1]')]

MFLOW_RT09 = STAT_THERM.AddMassFlowRate()
MFLOW_RT09.Location = NS_Passage9
MFLOW_RT09.Magnitude.Output.DiscreteValues = [Quantity('0[kg sec^-1]'), Quantity('-0.00499[kg sec^-1]')]

MFLOW_RT10 = STAT_THERM.AddMassFlowRate()
MFLOW_RT10.Location = NS_Passage10
MFLOW_RT10.Magnitude.Output.DiscreteValues = [Quantity('0[kg sec^-1]'), Quantity('-0.00253[kg sec^-1]')]

TEMP01 = STAT_THERM.AddTemperature()
TEMP01.Location = NS_Inlet1
TEMP01.Magnitude.Output.DiscreteValues = [Quantity('0[K]'), Quantity('348.83[K]')]

TEMP02 = STAT_THERM.AddTemperature()
TEMP02.Location = NS_Inlet2
TEMP02.Magnitude.Output.DiscreteValues = [Quantity('0[K]'), Quantity('349.32[K]')]

TEMP03 = STAT_THERM.AddTemperature()
TEMP03.Location = NS_Inlet3
TEMP03.Magnitude.Output.DiscreteValues = [Quantity('0[K]'), Quantity('339.49[K]')]

TEMP04 = STAT_THERM.AddTemperature()
TEMP04.Location = NS_Inlet4
TEMP04.Magnitude.Output.DiscreteValues = [Quantity('0[K]'), Quantity('342.3[K]')]

TEMP05 = STAT_THERM.AddTemperature()
TEMP05.Location = NS_Inlet5
TEMP05.Magnitude.Output.DiscreteValues = [Quantity('0[K]'), Quantity('333.99[K]')]

TEMP06 = STAT_THERM.AddTemperature()
TEMP06.Location = NS_Inlet6
TEMP06.Magnitude.Output.DiscreteValues = [Quantity('0[K]'), Quantity('364.95[K]')]

TEMP07 = STAT_THERM.AddTemperature()
TEMP07.Location = NS_Inlet7
TEMP07.Magnitude.Output.DiscreteValues = [Quantity('0[K]'), Quantity('343.37[K]')]

TEMP08 = STAT_THERM.AddTemperature()
TEMP08.Location = NS_Inlet8
TEMP08.Magnitude.Output.DiscreteValues = [Quantity('0[K]'), Quantity('365.41[K]')]

TEMP09 = STAT_THERM.AddTemperature()
TEMP09.Location = NS_Inlet9
TEMP09.Magnitude.Output.DiscreteValues = [Quantity('0[K]'), Quantity('408.78[K]')]

TEMP10 = STAT_THERM.AddTemperature()
TEMP10.Location = NS_Inlet10
TEMP10.Magnitude.Output.DiscreteValues = [Quantity('0[K]'), Quantity('453.18[K]')]

TEMP11 = STAT_THERM.AddTemperature()
TEMP11.Location = NS_Faces4
TEMP11.Magnitude.Output.DiscreteValues = [Quantity('0[K]'), Quantity('568[K]')]

TEMP_RST01 = STAT_THERM_SOLN.AddTemperature()
TEMP_RST01.Location = NS_Body1
TEMP_RST02 = STAT_THERM_SOLN.AddTemperature()
TEMP_RST02.Location = NS_Bodies10
TEMP_RST03 = STAT_THERM_SOLN.AddTemperature()
TEMP_RST03.ScopingMethod = GeometryDefineByType.ResultFileItem
TEMP_RST03.ItemType = ResultFileItemType.ElementNameIDs
TEMP_RST03.SolverComponentIDs = 'SURF152'
TEMP_RST04 = STAT_THERM_SOLN.AddTemperature()
TEMP_RST04.Location = PATH01
#TEMP_RST05 = STAT_THERM_SOLN.AddTemperature()
#TEMP_RST05.Location = PATH02

#ExtAPI.SelectionManager.AddSelection(NS_Body1)
#js = ExtAPI.Application.ScriptByName("jscript")
#TEMP_RST05.Activate()
#js.ExecuteCommand('$.DSSetDetail($.ID_GEOMETRY, $.DV_VAL_APPLY)' );

STAT_THERM_SOLN.Solve(True)

FIX_SUP01 = STAT_STRUC.AddFixedSupport()
FIX_SUP01.Location = NS_Face1

FIX_SUP02 = STAT_STRUC.AddFixedSupport()
FIX_SUP02.Location = NS_Face2

EQV_STRS01 = STAT_STRUC_SOLN.AddEquivalentStress()
EQV_STRS01.Location = NS_Body1
#EQV_STRS02 = STAT_STRUC_SOLN.AddEquivalentStress()
#EQV_STRS02.Location = PATH02

#ExtAPI.SelectionManager.AddSelection(NS_Body1)
#EQV_STRS02.Activate()
#js.ExecuteCommand('$.DSSetDetail($.ID_GEOMETRY, $.DV_VAL_APPLY)' );

STAT_STRUC_SOLN.Solve(True)

# Set isometric view and zoom to fit
cam = Graphics.Camera
cam.SetSpecificViewOrientation(ViewOrientationType.Iso)
cam.SetFit()

mechdir = STAT_STRUC.Children[0].SolverFilesDirectory
export_path = os.path.join(mechdir, "stress.png")
EQV_STRS01.Activate()
Graphics.ExportImage(export_path, GraphicsImageExportFormat.PNG)

results = { "Stress": str(EQV_STRS01.Maximum) }
json.dumps(results)