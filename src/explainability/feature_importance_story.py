def generate_feature_importance_story(insights):

    story = []

    story.append("MODEL DRIVERS")

    for insight in insights:

        story.append(f"• {insight}")

    return story