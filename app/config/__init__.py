from app.model.config import OptionGroup, Option
from app.util import singleton_instance


@singleton_instance
class LoginConfigGroup(OptionGroup):
    auto_create_user = Option()
