from dotenv import dotenv_values


ROW_COUNT: int = 25
BILL_ROW_COUNT: int = 18
PRODUCT_TYPES: dict[str, str] = {
    "tablet": "tab",
    "capsule": "cap",
    "syrup": "srp",
    "drops": "drp",
    "ointment": "ont",
    "cream": "crm",
    "gel": "gel",
    "powder": "pwd",
    "injection": "inj",
    "other": "oth"
}
PRODUCT_TYPES_LIST = [key.capitalize() for key in PRODUCT_TYPES.keys()]

LABEL_FONT = ("Aerial", 16)
ENTRY_FONT = ("Aerial", 14)
TABLE_HEADER_FONT = ("Aerial", 14)
TABLE_DATA_FONT = ("Aerial", 12)

env: dict[str, str | None] = dotenv_values(".env")
COMPANY_NAME: str = env.get("COMPANY_NAME", "Company Name")
COMPANY_ADDRESS: str = env.get("COMPANY_ADDRESS", "City-XX, District")
PAN_NO: str = env.get("PAN_NO", "0000000000")
DDA_NO: str = env.get("DDA_NO", "0000000000/000")
