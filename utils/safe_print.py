#You should have received a copy of the GNU General Public License along with Logic Evaluation Engine (LEE). If not, see <https://www.gnu.org/licenses/>.

#

# utils/safe_print.py

import sys

def safe_print(text: str):
    """
    Prints Unicode-safe text to the terminal.
    Falls back gracefully if the terminal encoding can't handle certain characters.
    """
    try:
        print(text)
    except UnicodeEncodeError:
        print(text.encode('ascii', 'backslashreplace').decode())