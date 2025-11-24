# fetch_menu.py 
from playwright.sync_api import sync_playwright
import json
from datetime import date
from pathlib import Path

HUDS_URL_TEMPLATE = (
    "https://www.foodpro.huds.harvard.edu/foodpro/"
    "shtmenu.aspx?sName=HARVARD+UNIVERSITY+DINING+SERVICES"
    "&locationNum=30&locationName=Dining+Hall"
    "&naFlag=1&WeeksMenus=This+Week%27s+Menus"
    "&myaction=read&dtdate={date}"
)

def dedup(seq):
    """Remove duplicates while preserving order."""
    seen = set()
    out = []
    for x in seq:
        if x not in seen:
            seen.add(x)
            out.append(x)
    return out

def scrape_menu_for_today():
    today = date.today()
    date_str = today.strftime("%m/%d/%Y")
    url = HUDS_URL_TEMPLATE.format(date=date_str)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        print(f"Opening: {url}")
        page.goto(url)
        page.wait_for_load_state("networkidle")

        # JS in page: categorize by meal (Lunch/Dinner) and category headings
        categories_by_meal = page.evaluate(
            """
            () => {
              const data = {};

              const mealMap = {
                "LUNCH": "Lunch",
                "DINNER": "Dinner"
              };

              const catsMap = {
                "SOUP": "Today's Soup",
                "ENTREE": "Entrees",
                "ENTREES": "Entrees",
                "DESSERT": "Desserts",
                "DESSERTS": "Desserts",
                "SIDE": "Sides",
                "SIDES": "Sides",
                "STARCH": "Starch",
                "STARCHES": "Starch",
                "BRAIN BREAK": "Brain Break",
                "BRUNCH": "Brunch"
              };

              let currentMeal = null;
              let currentCat = null;

              const rows = Array.from(
                document.querySelectorAll("td[valign='top'] table tr")
              );

              for (const row of rows) {
                const txt = row.innerText.trim();
                if (!txt) continue;
                const upper = txt.toUpperCase();

                // Check if this row has a menu item
                const itemSpan = row.querySelector("div.shortmenurecipes span");

                // If it's a heading row (no itemSpan)
                if (!itemSpan) {
                  // 1) Meal heading (Lunch / Dinner)
                  const mealKey = Object.keys(mealMap).find(key =>
                    upper.includes(key)
                  );
                  if (mealKey) {
                    currentMeal = mealMap[mealKey];
                    if (!data[currentMeal]) data[currentMeal] = {};
                    currentCat = null;
                    continue;
                  }

                  // Ignore anything before we know which meal we're in
                  if (!currentMeal) {
                    continue;
                  }

                  // 2) Category heading we actually care about
                  const catKey = Object.keys(catsMap).find(key =>
                    upper.includes(key)
                  );
                  if (catKey) {
                    const catName = catsMap[catKey];
                    currentCat = catName;
                    if (!data[currentMeal][currentCat]) {
                      data[currentMeal][currentCat] = [];
                    }
                    continue;
                  }

                  // 3) Any other non-item row is a "stop" header:
                  //    stop adding to the previous category
                  currentCat = null;
                  continue;
                }

                // If we get here, it's a food item row (has itemSpan),
                // so NEVER treat it as a heading even if it contains words
                // like "SOUP" or "ENTREE".
                if (currentMeal && currentCat) {
                  let itemText = itemSpan.innerText.replace(/\\u00A0/g, " ").trim();
                  if (itemText) {
                    data[currentMeal][currentCat].push(itemText);
                  }
                }
              }

              return data;
            }
            """
        )

        browser.close()

    # Build ordered lists for lunch and dinner
    desired_order = [
        "Today's Soup",
        "Brunch",
        "Entrees",
        "Starch",
        "Sides",
        "Desserts",
        "Brain Break",
    ]

    def build_meal_list(meal_name: str):
        meal_cats = categories_by_meal.get(meal_name, {})
        out = []
        for cat in desired_order:
            items = meal_cats.get(cat, [])
            items = dedup(items)
            if items:
                out.append({"name": cat, "items": items})
        return out

    lunch_list = build_meal_list("Lunch")
    dinner_list = build_meal_list("Dinner")

    data = {
        "date": date_str,
        "lunch": lunch_list,
        "dinner": dinner_list,
    }

    data_dir = Path("data")
    data_dir.mkdir(exist_ok=True)
    out_path = data_dir / "menu_today.json"

    with out_path.open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"Saved categorized menu (lunch + dinner) to {out_path}")


if __name__ == "__main__":
    scrape_menu_for_today()
