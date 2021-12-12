from renderer.main import MainRenderer
from rgbmatrix import RGBMatrix
from utils import args, led_matrix_options
import debug

SCRIPT_NAME = "Message Flexer Hell Yeah Brother"
SCRIPT_VERSION = "0.0.1"

# Get supplied command line arguments
args = args()

# Check for led configuration arguments
matrixOptions = led_matrix_options(args)

# Initialize the matrix
matrix = RGBMatrix(options = matrixOptions)

# Print some basic info on startup
debug.info("{} - v{} ({}x{})".format(SCRIPT_NAME, SCRIPT_VERSION, matrix.width, matrix.height))

# Read scoreboard options from config.json if it exists
# config = ScoreboardConfig("config", args)
# debug.set_debug_status(config)

# data = Data(config)

MainRenderer(matrix).render()