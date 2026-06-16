def generate_recommendation_story(recommendations):

    story = []

    story.append("RECOMMENDATIONS")

    for recommendation in recommendations:

        story.append(f"• {recommendation}")

    return story