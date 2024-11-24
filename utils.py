import matplotlib.pyplot as plt
from textwrap import fill

def create_box(ax, x, y, width, height, text, fontsize=8):
    """Create a box with wrapped text"""
    rect = plt.Rectangle((x, y), width, height, 
                        facecolor='white',
                        edgecolor='black',
                        linewidth=1,
                        alpha=1,
                        zorder=1)
    ax.add_patch(rect)
    
    wrapped_text = fill(text, width=30)
    ax.text(x + width/2, y + height/2, wrapped_text,
            horizontalalignment='center',
            verticalalignment='center',
            fontsize=fontsize,
            zorder=2)
    
    return (x + width/2, y + height/2)  # Return center coordinates

def create_arrow(ax, start, end):
    """Create an arrow between boxes"""
    ax.annotate('',
               xy=end,
               xytext=start,
               arrowprops=dict(arrowstyle='->',
                              connectionstyle='arc3,rad=0',
                              linewidth=1,
                              zorder=1))

def create_prisma_diagram(values):
    """Create the PRISMA flow diagram"""
    fig, ax = plt.subplots(figsize=(12, 16))
    plt.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.1)
    
    # Set the plot limits
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    
    # Create boxes and store their centers
    # Identification
    db_center = create_box(ax, 20, 85, 25, 8, 
                          f'Records identified from databases (n = {values["databases"]})')
    other_center = create_box(ax, 55, 85, 25, 8,
                            f'Records from other sources (n = {values["other_sources"]})')
    
    # Screening
    duplicates_center = create_box(ax, 37.5, 70, 25, 8,
                                 f'Records after duplicates removed (n = {values["records_screened"]})')
    screened_center = create_box(ax, 37.5, 55, 25, 8,
                               f'Records screened (n = {values["records_screened"]})')
    excluded_center = create_box(ax, 70, 55, 25, 8,
                               f'Records excluded (n = {values["records_excluded"]})')
    
    # Eligibility
    fulltext_center = create_box(ax, 37.5, 40, 25, 8,
                               f'Full-text articles assessed (n = {values["full_text"]})')
    excluded_ft_center = create_box(ax, 70, 40, 25, 15,
                                  f'Full-text articles excluded (n = {values["excluded_total"]}):\n' +
                                  f'• Irrelevant outcome (n = {values["irrelevant"]})\n' +
                                  f'• Low quality (n = {values["low_quality"]})\n' +
                                  f'• Duplicates (n = {values["duplicates_ft"]})\n' +
                                  f'• Not related (n = {values["not_related"]})')
    
    # Included
    qual_center = create_box(ax, 37.5, 25, 25, 8,
                           f'Studies included in qualitative synthesis (n = {values["qualitative"]})')
    quant_center = create_box(ax, 37.5, 10, 25, 8,
                            f'Studies included in quantitative synthesis (n = {values["quantitative"]})')
    
    # Create arrows with proper connections
    create_arrow(ax, db_center, (duplicates_center[0], duplicates_center[1] + 4))
    create_arrow(ax, other_center, (duplicates_center[0], duplicates_center[1] + 4))
    create_arrow(ax, (duplicates_center[0], duplicates_center[1] - 4), (screened_center[0], screened_center[1] + 4))
    create_arrow(ax, (screened_center[0] + 12.5, screened_center[1]), excluded_center)
    create_arrow(ax, (screened_center[0], screened_center[1] - 4), (fulltext_center[0], fulltext_center[1] + 4))
    create_arrow(ax, (fulltext_center[0] + 12.5, fulltext_center[1]), excluded_ft_center)
    create_arrow(ax, (fulltext_center[0], fulltext_center[1] - 4), (qual_center[0], qual_center[1] + 4))
    create_arrow(ax, (qual_center[0], qual_center[1] - 4), (quant_center[0], quant_center[1] + 4))
    
    # Remove axes
    ax.axis('off')
    
    # Add title
    plt.title('PRISMA Flow Diagram', pad=20, size=14)
    
    return fig