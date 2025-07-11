#This file is part of Logic Evaluation Engine.
#Logic Evaluation Engine is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
#Logic Evaluation Engine is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
#You should have received a copy of the GNU General Public License along with Logic Evaluation Engine.
#If not, see https://www.gnu.org/licenses/.

#

from enum import Enum

class State(Enum):
    ALIVE = "Alive"
    JAM = "Jam"
    MEM = "Mem"
    VAC = "Vac"
