from app.bps.api.result.code import result_code_map
from app.model.config import Config


globals_dict = {
    'ext_config': Config,
    'result_code': result_code_map()
}
