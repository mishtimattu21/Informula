from supabase_client import get_user_profile
from prompt_formatter import format_prompt
from gemini_client import get_ingredient_report
from processing import extract_text_from_image

def main():
    # Sample user ID — must match one from your Supabase table
    user_id = input("Enter user UUID: ").strip()
    
    # Step 1: Get user profile
    user_profile = get_user_profile(user_id)
    if not user_profile:
        print("❌ User not found.")
        return

    # Step 2: Extract text from image
    print("\n📸 Processing image...")
    try:
        ingredients_input = extract_text_from_image()
        print("\n✅ Image processed successfully!")
    except Exception as e:
        print(f"❌ Error processing image: {str(e)}")
        return

    # Step 3: Format prompt
    prompt = format_prompt(ingredients_input, user_profile)

    # Step 4: Get Gemini response
    print("\n🔄 Generating your safety analysis...\n")
    result = get_ingredient_report(prompt)
    print("✅ Result:\n")
    print(result)

if __name__ == "__main__":
    main()
