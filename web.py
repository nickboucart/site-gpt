import gradio as gr
import website_to_kb as w2kb


def answerQuestion(website, question):
    response = w2kb.questionAndAnswer(website, question)
    return response.content

def pdfQuestion(pdfCollection, question):
    response = w2kb.pdfQuestion(pdfCollection, question)
    return response.content

def loadWebsite(url, progress=gr.Progress()):
    return w2kb.storeWebsiteInDb(url, progress)

with gr.Blocks() as demo:
    gr.Markdown("# Demo van enkele dingen die we zouden kunnen doen met llms")
    with gr.Tab("website checker"):
        gr.Markdown("## Laad een website in en stel vragen die volgens jou beantwoord moeten worden door deze website")
        gr.Markdown("Deze app download alle webpagina's die het vindt via een sitemap.xml, en gebruikt die content om vragen te beantwoorden.\nStel vragen zoals jij denkt dat klanten ze zouden stellen. Als de antwoorden niet zijn wat je verwacht, is de kans groot dat de inhoud van je website beter moet. ")
        website = gr.Textbox(max_lines=1, label="Website URL", info="https://www.sirris.be")
        gr.Interface(fn=loadWebsite, inputs=website, outputs="text")
        question = gr.Textbox(max_lines=1, label="uw vraag")
        gr.Interface(fn=answerQuestion, inputs=[website, question], outputs="text")
    with gr.Tab("pdf bot"):
        gr.Markdown("## Stel vragen aan een collectie pdfs.")
        collection = gr.Dropdown(choices=["asvs", "roadmaps"], value="roadmaps", label="Selecteer de pdf collectie waarmee je wil chatten.")
        gr.Interface(fn=pdfQuestion, inputs=[collection, "text"], outputs="text")
    # with gr.Tab("Linkedin Post Generator"):
    #     gr.Markdown("## maak een engaging linkedin post op basis van een blog artikel")
    # with gr.Tab("landing page"):
    #     gr.Markdown("## Beschrijf je startup idee en genereer een basis-idee voor landing page")



if __name__ == "__main__":
    demo.launch(show_api=False)