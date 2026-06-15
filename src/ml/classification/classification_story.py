def generate_classification_story(insights):

    story = []

    story.append("CLASSIFICATION MODEL PERFORMANCE")

    for insight in insights:

        story.append(f"• {insight}")


    return story