from supabase import create_client

SUPABASE_URL = "https://qsuqihxanwdjgkuzambz.supabase.co"
SUPABASE_KEY = "sb_publishable_XOx9WaW2ZjLAK8Z8QDwj2A_Ds3rArJu"

supabase = create_client(
    SUPABASE_URL,
    SUPABASE_KEY
)

print("Supabase connected successfully!")

# Test the resources table
response = supabase.table("RESOURCES").select("*").execute()

print("Resources data:")
print(response.data)