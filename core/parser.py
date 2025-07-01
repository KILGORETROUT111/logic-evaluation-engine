#This file is part of Logic Evaluation Engine.
#Logic Evaluation Engine is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
#Logic Evaluation Engine is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
#You should have received a copy of the GNU General Public License along with Logic Evaluation Engine.
#If not, see <https://www.gnu.org/licenses/>.

#

from core.expressions import Functor, Value, Var

def build(obj):
    print("🔍 Parsing:", obj)

    if isinstance(obj, list):
        head = obj[0]
        args = obj[1:]
        parsed_args = [build(arg) for arg in args]
        return Functor(str(head).upper(), parsed_args)

    elif isinstance(obj, dict):
        if "value" in obj:
            return Value(obj["value"])
        else:
            raise ValueError(f"Unsupported dict format: {obj}")

    elif isinstance(obj, (int, float)):
        return Value(obj)

    elif isinstance(obj, str):
        if obj.isidentifier():
            return Var(obj)
        return Value(obj)

    else:
        raise ValueError(f"Unsupported expression type: {type(obj)}")

def parse_expression(obj):
    return build(obj)