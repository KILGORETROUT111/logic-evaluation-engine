#You should have received a copy of the GNU General Public License along with Logic Evaluation Engine (LEE). If not, see <https://www.gnu.org/licenses/>.

# trace_json_test.py

from core.evaluation import evaluate_full
from core.expressions import Lambda, Variable, Application, Literal
import sys
import os
sys.path.append(os.path.abspath('.'))

from utils.trace_export import emit_trace_to_json

# Define the expression: ((λx.x) 42)
expr = Application(
    Lambda("x", Variable("x")),
    Literal(42)
)

# Evaluate and capture trace
result, trace = evaluate_full(expr)

# Emit to JSON under root/out/trace_output.json
output_path = os.path.abspath(os.path.join("out", "trace_output.json"))
os.makedirs(os.path.dirname(output_path), exist_ok=True)
emit_trace_to_json(trace, output_path)

print("✅ JSON trace exported to:", output_path)