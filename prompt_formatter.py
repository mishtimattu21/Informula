def format_prompt(ingredients_input, user_profile, prod_name=None, prod_desc=None):
    product_info = ""
    if prod_name:
        product_info += f"📦 PRODUCT_NAME: {prod_name}\n"
    if prod_desc:
        product_info += f"📝 USER_DESCRIPTION: {prod_desc}\n"

    return f"""
You are a certified ingredient safety analyst.

A user has uploaded a product's ingredient list and profile. Analyze each ingredient **individually** using expert medical, toxicological, and regulatory knowledge.

---

🧪 INGREDIENTS_INPUT:
{ingredients_input.strip()}

{product_info.strip()}

👤 USER_PROFILE:
- AGE: {user_profile['age']}
- GENDER: {user_profile['gender']}
- PAST_MEDICATIONS: {', '.join(user_profile['past_medication'])}
- ALLERGIES: {', '.join(user_profile['allergies'])}
- AVOID_LIST: {', '.join(user_profile['avoid_list'])}

---

🎯 YOUR TASK:

For **each ingredient**, return a block following this format exactly:

---

INGREDIENT_NAME: <name>  
STATUS: ✅ Safe / ⚠️ Caution / 🚫 Dangerous  
USAGE:  
- Bullet points summarizing what it’s used for and why it has this safety rating  
- If applicable, add:  
  - 🧬 User-specific risk (only if allergy, medication, age, or avoid list applies)  
  - 🌍 Banned in [Country1, Country2] (if applicable)  
  - 📚 Significant findings from studies (2020–2024) — only if they suggest real concern  
  - 📏 Safe usage threshold (e.g., "Max 0.5% daily use")  
  - ⚠️ Interaction warnings (e.g., "Do not mix with acids or retinoids")  
SOURCES:  
- Add only if you cited a **ban, study, threshold, or warning**  
- Use links to studies, regulations, or clinical guidelines (max 2)

---

📌 Keep output clean and consistent — this will be parsed using regex  
📌 Do NOT output section headings unless required (like SOURCES:)  
📌 Skip blank sections — only show what applies  
📌 Combine everything under USAGE as bullet points  
📌 Never guess studies — only cite if source-worthy  
📌 No summaries or greetings — just the ingredient blocks
"""
