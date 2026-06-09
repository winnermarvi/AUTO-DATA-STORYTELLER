#Giving the insight from insight generator

def generate_story(insights): 


    story = []

    section_titles = {
        "overview": "DATASET OVERVIEW",
        "data_quality": "DATA QUALITY",
        "numerical": "NUMERICAL INSIGHTS",
        "categorical": "CATEGORICAL INSIGHTS",
        "relationship": "RELATIONSHIPS"
    }

    for key, values in insights.items():

        story.append(section_titles[key])

        if len(values) > 0:

            for line in values:
                story.append(f"• {line}")

        else:

            if key == "relationship":
                story.append("• No strong relationships were identified.")
            else:
                story.append("• No significant findings identified.")

        story.append("")

    return story