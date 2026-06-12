
def generate_regression_story(insights):

    story = []

    story.append("MODEL PERFORMANCE")

    for insight in insights:

        story.append(f"• {insight}")


    return story