import streamlit as st
import graphviz

# Page setup
st.title("PRISMA Flow Diagram Generator")

# Input fields
st.header("Enter your PRISMA numbers")

# Identification section
st.subheader("Identification")
databases = st.number_input("Records from databases (n)", value=200)
other_sources = st.number_input("Records from other sources (n)", value=20)
duplicates = st.number_input("Records removed (duplicates) (n)", value=40)
records_screened = st.number_input("Records screened (n)", value=180)
records_excluded = st.number_input("Records excluded (n)", value=130)

# Full-text section
st.subheader("Full-text Assessment")
full_text = st.number_input("Full-text articles assessed (n)", value=50)
excluded_total = st.number_input("Full-text articles excluded (n)", value=35)

# Reasons for exclusion
st.subheader("Reasons for Exclusion")
irrelevant = st.number_input("- Irrelevant outcome measures (n)", value=12)
low_quality = st.number_input("- Low-quality methodology (n)", value=10)
duplicates_ft = st.number_input("- Duplicates (n)", value=8)
not_related = st.number_input("- Not related to topic (n)", value=5)

# Inclusion section
st.subheader("Inclusion")
qualitative = st.number_input("Studies in qualitative synthesis (n)", value=15)
quantitative = st.number_input("Studies in quantitative synthesis (n)", value=7)

def create_prisma_diagram():
    # Create a new directed graph
    dot = graphviz.Digraph()
    dot.attr(rankdir='TB')
    
    # Node attributes for professional looking boxes
    dot.attr('node', shape='box', 
            style='rounded,filled', 
            fillcolor='white',
            margin='0.2',
            fontname='Arial')
    
    # Edge attributes for clean arrows
    dot.attr('edge', arrowsize='0.8')
    
    # Add nodes with proper formatting
    dot.node('db', f'Records identified from databases\n(n = {databases})')
    dot.node('other', f'Records from other sources\n(n = {other_sources})')
    dot.node('duplicates', f'Records after duplicates removed\n(n = {records_screened})')
    dot.node('screened', f'Records screened\n(n = {records_screened})')
    dot.node('excluded', f'Records excluded\n(n = {records_excluded})')
    dot.node('full_text', f'Full-text articles assessed\n(n = {full_text})')
    dot.node('excluded_ft', f'Full-text articles excluded (n = {excluded_total}):\n' +
             f'• Irrelevant outcome (n = {irrelevant})\n' +
             f'• Low quality (n = {low_quality})\n' +
             f'• Duplicates (n = {duplicates_ft})\n' +
             f'• Not related (n = {not_related})')
    dot.node('qualitative', f'Studies included in\nqualitative synthesis\n(n = {qualitative})')
    dot.node('quantitative', f'Studies included in\nquantitative synthesis\n(n = {quantitative})')
    
    # Add edges with proper spacing
    dot.edge('db', 'duplicates')
    dot.edge('other', 'duplicates')
    dot.edge('duplicates', 'screened')
    dot.edge('screened', 'excluded')
    dot.edge('screened', 'full_text')
    dot.edge('full_text', 'excluded_ft')
    dot.edge('full_text', 'qualitative')
    dot.edge('qualitative', 'quantitative')
    
    return dot

if st.button("Generate PRISMA Flow Diagram", type="primary"):
    try:
        # Create and display the diagram
        dot = create_prisma_diagram()
        st.graphviz_chart(dot)
        
        # Generate PNG for download
        dot.format = 'png'
        png_data = dot.pipe()
        
        # Add download button
        st.download_button(
            label="⬇️ Download PRISMA Diagram",
            data=png_data,
            file_name="prisma_flow_diagram.png",
            mime="image/png"
        )
        
        st.success("✅ Diagram generated successfully! Click the download button above to save it.")
        
    except Exception as e:
        st.error(f"""
        ⚠️ An error occurred while generating the diagram. 
        Please try again or contact support if the problem persists.
        
        Error details: {str(e)}
        """)

# Add instructions
st.markdown("""
---
### How to use:
1. Enter your numbers in the input fields
2. Click 'Generate PRISMA Flow Diagram'
3. Download the diagram using the download button that appears below the diagram

### About PRISMA Flow Diagrams
PRISMA (Preferred Reporting Items for Systematic Reviews and Meta-Analyses) flow diagrams are essential for transparent reporting of systematic reviews and meta-analyses. They show the flow of information through different phases of the review process.
""")