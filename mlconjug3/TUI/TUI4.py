import textual
from .mlconjug import Conjugator
import json
import logging
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from PIL import Image, ImageDraw, ImageFont
import requests
from bs4 import BeautifulSoup
# TODO fix interface inconsistencies.

class TUI:
    def init(self):
        self.app = textual.Application(title="Verb Conjugator")
        self.left_section = self.app.add(textual.Container(flex=1))
        self.right_section = self.app.add(textual.Container(flex=1))
        self.prompt = self.left_section.add(textual.Prompt(placeholder="Enter a verb"))
        self.conjugation_tables = self.left_section.add(textual.Container(flex=1))
        self.verb_history = self.right_section.add(textual.List(flex=1))
        self.sample_verbs = self.right_section.add(textual.List(flex=1))
        self.export_button = self.right_section.add(textual.Button("Export"))
        self.language_selector = self.right_section.add(textual.Select(options=["fr", "en", "es", "it", "pt", "ro"]))
        self.subject_selector = self.right_section.add(textual.Select(options=["abbrev", "pronoun"]))
        self.template_selector = self.right_section.add(textual.Select(options=DataSet.templates))
        self.template_selector.on_select(self.handle_template_select)
        self.grid_view_button = self.right_section.add(textual.Button("Grid View"))
        self.image_view_button = self.right_section.add(textual.Button("Image View"))
        self.grid_view_button.on_click(self.handle_grid_view)
        self.image_view_button.on_click(self.handle_image_view)
        self.help_section = self.right_section.add(textual.Container(flex=1))
        self.app.add_stylesheet("dark.css")
        self.add_dark_mode_button()

        self.conjugator = Conjugator()
        self.prompt.on_submit(self.handle_submit)
        self.export_button.on_click(self.handle_export)
        self.verb_history.on_select(self.handle_history_select)
        self.language_selector.on_select(self.handle_language_select)
        self.subject_selector.on_select(self.handle_subject_select)
        self.help_section.add(textual.Text("Enter a verb in the prompt to conjugate it. Use the export button to save the conjugations. Use the language selector to choose the language for conjugation. Use the subject selector to choose between abbrev or pronoun for conjugations"))
        
    @staticmethod
    def get_verb_examples_in_context(verb):
        """
        Retrieves examples of the provided verb used in context from an external website.
        :param verb: string. The verb to retrieve examples for.
        :return: list of strings. A list of examples of the verb used in context.
        """
        url = f"https://context.reverso.net/translation/{verb}-examples"
        page = requests.get(url)
        soup = BeautifulSoup(page.content, "html.parser")
        examples = soup.find_all("a", class_="example-sentence")
        return [example.get_text() for example in examples]
    
    def handle_submit(self, verb):
        self.conjugator.set_language(self.language_selector.get_value())
        conjugation_result = self.conjugator.conjugate(verb, self.subject_selector.get_value())
        if conjugation_result:
            self.verb_history.add_item(verb)
            self.conjugation_tables.clear()
            
            self.grid_button = self.right_section.add(textual.Button("Grid View"))
            self.grid_button.on_click(self.handle_grid_view)
            
            self.image_button = self.right_section.add(textual.Button("Image View"))
            self.image_button.on_click(self.handle_image_view)
            
            self.both_button = self.right_section.add(textual.Button("Both View"))
            self.both_button.on_click(self.handle_both_view)
            
            self.handle_grid_view(verb, conjugation_result)
            
    def handle_submit(self, verb):
        self.conjugator.language = self.language
        self.conjugator.subject = self.subject
        self.conjugation_tables.clear()
        verb_info = self.conjugator.conjugate(verb)
        if verb_info:
            self.display_verb_conjugations(verb, verb_info)
            self.verb_history.append(verb)
        else:
            self.conjugation_tables.add(textual.Text(f"The verb {verb} is not in the {self.conjugator.language} verb database"))
    
            
    def handle_grid_view(self, verb, conjugation_result):
        """
        Displays the conjugations in a grid view
        """
        for tense, conjugations in conjugation_result.items():
            tense_container = self.conjugation_tables.add(textual.Container())
            tense_container.add(textual.Label(tense))
            conjugation_table = tense_container.add(textual.Table(headers=["Subject", "Conjugation"]))
            for subject, conjugation in conjugations.items():
                conjugation_table.add_row([subject, conjugation])
            examples = get_verb_examples_in_context(verb)
            if examples:
                self.sample_verbs.clear()
                for example in examples:
                    self.sample_verbs.add_item(example)
                self.conjugation_table_view = self.left_section.add(textual.ToggleButton(options=["Grid View", "Image View"], selected_index=0))
            self.conjugation_table_view.on_select(self.handle_conjugation_table_view)

            
    def handle_image_view(self):
        self.conjugation_tables.clear()
        for tense, conjugations in conjugation_result.items():
            tense_container = self.conjugation_tables.add(textual.Container())
            tense_container.add(textual.Label(tense))
            for subject, conjugation in conjugations.items():
                image = self.generate_image_for_conjugation(tense, subject, conjugation)
                tense_container.add(textual.Image(image))
                
    def generate_image_for_conjugation(self, tense, subject, conjugation):
        """
        Generates an image of the conjugation using a charting library
        :param tense: str, the tense of the conjugation
        :param subject: str, the subject of the conjugation
        :param conjugation: str, the conjugation itself
        :return: PIL Image, an image of the conjugation
        """
        # Create a blank image with a white background
        image = Image.new("RGB", (600, 100), color=(255, 255, 255))

        # Create a draw object to draw on the image
        draw = ImageDraw.Draw(image)

        # Add the tense, subject, and conjugation to the image
        font = ImageFont.truetype("arial.ttf", 40)
        draw.text((10, 10), tense, font=font, fill=(0, 0, 0))
        draw.text((10, 50), subject, font=font, fill=(0, 0, 0))
        draw.text((300, 50), conjugation, font=font, fill=(0, 0, 0))

        return image
    
    def handle_conjugation_table_view(self, selected_index):
        if selected_index == 0:
            self.handle_grid_view(verb, conjugation_result)
        elif selected_index == 1:
            self.handle_image_view(verb, conjugation_result)

            
    def show_grid_view(self):
        self.conjugation_tables.clear()
        for tense, conjugations in conjugation_result.items():
            tense_container = self.conjugation_tables.add(textual.Container())
            tense_container.add(textual.Label(tense))
            conjugation_table = tense_container.add(textual.Table(headers=["Subject", "Conjugation"]))
            for subject, conjugation in conjugations.items():
                conjugation_table.add_row([subject, conjugation])
    
    def show_image_view(self):
        self.conjugation_tables.clear()
        for tense, conjugations in conjugation_result.items():
            tense_container = self.conjugation_tables.add(textual.Container())
            tense_container.add(textual.Label(tense))
            for subject, conjugation in conjugations.items():
                image = self.generate_image_for_conjugation(tense, subject, conjugation)
                tense_container.add(textual.Image(image))
    
    def handle_history_select(self, verb):
        """
        Handles the verb history list select event.
        Displays the conjugations for the selected verb.
        """
        self.prompt.set_text(verb)
        conjugation_result = self.conjugator.conjugate(verb, self.subject_selector.get_value())
        if conjugation_result:
            self.conjugation_tables.clear()
            for tense, conjugations in conjugation_result.items():
                tense_container = self.conjugation_tables.add(textual.Container())
                tense_container.add(textual.Label(tense))
                conjugation_table = tense_container.add(textual.Table(headers=["Subject", "Conjugation"]))
                for subject, conjugation in conjugations.items():
                    conjugation_table.add_row([subject, conjugation])
        else:
            self.conjugation_tables.clear()
            self.conjugation_tables.add(textual.Text("The verb is not in the dataset. The conjugation was not possible."))
        
    def handle_export(self):
        export_format = textual.dialog.ask("What format do you want to export?", ["JSON", "CSV"])
        if export_format:
            export_path = textual.dialog.ask("Where do you want to save the file?", "file")
        if export_path:
            with open(export_path, 'w', encoding='utf-8') as file:
                json.dump(self.conjugation_tables, file, ensure_ascii=False, indent=4)
                textual.alert("The conjugations have been succesfully saved to {0}.".format(export_path))
        self.app.focus(self.export_button)

    def handle_language_select(self, language):
        self.conjugator.set_language(language)
        self.prompt.set_value('')
        self.conjugation_tables.clear()
        self.sample_verbs.clear()

    def handle_subject_select(self, subject):
        self.handle_submit(self.prompt.get_value())
        self.app.focus(self.subject_selector)
    
    def handle_similar_verb_select(self, verb):
        self.prompt.set_value(verb)
        self.handle_submit(verb)
        self.app.focus(self.prompt)
            
    def display_conjugations_in_table(self, conjugations):
        self.conjugation_tables.clear()
        headers = ["Person", "Singular", "Plural"]
        rows = []
        for person, conjugation in conjugations.items():
            rows.append([person, conjugation["singular"], conjugation["plural"]])
        table = textual.Table(headers=headers, rows=rows)
        self.conjugation_tables.add(table)
    
    def change_verb_tense(self):
        self.tense_selector = self.right_section.add(textual.Select(options=["present", "past", "future", "subjunctive", "conditional"]))
        self.tense_selector.on_select(self.handle_tense_change)

    def handle_tense_change(self, selection):
        self.tense = selection
        self.handle_submit(self.verb_input.value)
    
    def handle_template_select(self, new_template):
        """
        Method to handle when user selects a new template to re-conjugate the current verb.
        :param new_template: string. The new template selected by the user
        """
        current_verb = self.verb_history.get_selected()
        current_verb.verb_info.template = new_template
        self.conjugator.set_language(self.language_selector.get_value())
        conjugation_result = self.conjugator.conjugate(current_verb, self.subject_selector.get_value())
        if conjugation_result:
            self.conjugation_tables.clear()
            for tense, conjugations in conjugation_result.items():
                tense_container = self.conjugation_tables.add(textual.Container())
                tense_container.add(textual.Label(tense))
                conjugation_table = tense_container.add(textual.Table(headers=["Subject", "Conjugation"]))
                for subject, conjugation in conjugations.items():
                    conjugation_table.add_row([subject, conjugation])
        else:
            self.conjugation_tables.clear()
            self.conjugation_tables.add(textual.Text("The verb is not in the dataset. The conjugation was not possible."))
        
    
    def compare_multiple_conjugations(self):
        self.multiple_verb_input = self.left_section.add(textual.Prompt(placeholder="Enter multiple verbs separated by commas"))
        self.multiple_verb_input.on_submit(self.handle_multiple_submit)

    def handle_multiple_submit(self, input_text):
        verbs = input_text.split(',')
        results = {}
        for verb in verbs:
            result = self.conjugator.conjugate(verb.strip(), self.subject)
            results[verb.strip()] = result.conjug_info
        self.conjugation_tables.clear()
        for verb, conjugations in results.items():
            verb_table = self.conjugation_tables.add(textual.Table(flex=1))
            verb_table.add_column("Tense/Person", flex=1)
            verb_table.add_column(verb, flex=1)
            for tense, conjugation in conjugations.items():
                verb_table.add_row(tense, conjugation)
        self.verb_history.append(input_text)
    
    def filter_conjugations_by_person_number_mood(self, verb_info, person, number, mood):
        filtered_conjugations = {}
        for key, value in verb_info.conjug_info.items():
            if key.endswith(person + number + mood):
                filtered_conjugations[key] = value
        return filtered_conjugations
    
    def handle_clear_filter(self):
        self.person_selector.clear_value()
        self.number_selector.clear_value()
        self.mood_selector.clear_value()
        self.conjugation_tables.clear()
        verb = self.verb_history.get_selected()
        if verb:
            verb_info = self.conjugator.conjugate(verb)
            self.display_verb_conjugations(verb, verb_info)


    def change_font_size_and_type(self, size, font_type):
    self.app.renders()
    self.app.add_stylesheet(f"{font_type}-{size}.css")

        
    def save_conjugation_history(self, verb, conjugations):
        """
        Save the conjugation history in a list and display it in the verb history section of the TUI
        :param verb: str, the verb that was conjugated
        :param conjugations: dict, the conjugations of the verb
        """
        self.verb_history.append(verb)
        self.conjugation_history[verb] = conjugations
        self.verb_history.update()
        
    def compare_conjugations_multiple_languages(self, verb):
        """
        Compares the conjugations of the given verb in multiple languages by conjugating the verb for all languages and displaying the conjugations in the conjugation_tables widget
        """
        self.conjugation_tables.clear()
        for language in self.language_selector.options:
            self.conjugator.set_language(language)
            conjugations = self.conjugator.conjugate(verb, self.subject_selector.value)
            self.conjugation_tables.add(textual.Text(f"Conjugations for {verb} in {language}:"))
            for key, value in conjugations.items():
                self.conjugation_tables.add(textual.Text(f"{key}: {value}"))
        
    def switch_layout_styles_themes(self):
        """
        Allows users to switch between different layout styles and themes
        """
        self.app.add(textual.Select(options=["Layout Style 1", "Layout Style 2", "Layout Style 3"]))
        self.app.add(textual.Select(options=["Theme 1", "Theme 2", "Theme 3"]))

    def handle_layout_change(self, layout_style):
        """
        handle the change event of the layout style selector by changing the layout style of the application
        """
        if layout_style == "Layout Style 1":
            self.app.layout_style = "layout_style_1"
        elif layout_style == "Layout Style 2":
            self.app.layout_style = "layout_style_2"
        elif layout_style == "Layout Style 3":
            self.app.layout_style = "layout_style_3"
        self.app.on_layout_change(handle_layout_change)

    def handle_theme_change(self, theme):
        """
        handle the change event of the theme selector by changing the theme of the application
        """
        if theme == "Theme 1":
            self.app.theme = "theme_1"
        elif theme == "Theme 2":
            self.app.theme = "theme_2"
        elif theme == "Theme 3":
            self.app.theme = "theme_3"
        self.app.on_theme_change(handle_theme_change)
        
    def add_dark_mode_button(self):
        """
        Add a button to toggle between dark mode and light mode
        """
        self.dark_mode_button = self.right_section.add(textual.Button("Dark Mode"))
        self.dark_mode_button.on_click(self.handle_dark_mode_toggle)
    
    def handle_dark_mode_toggle(self):
        """
        Handle the on_click event for the dark mode button by toggling between dark mode and light mode
        """
        current_mode = self.app.get_stylesheet()
        if current_mode == "dark":
            self.app.set_stylesheet("light")
        else:
            self.app.set_stylesheet("dark")


    def display_verb_examples_in_context(self, verb):
        """
        Display examples of the verb in context in the sample_verbs widget
        """
        examples = self.get_verb_examples_in_context(verb)
        self.sample_verbs.items = examples
        self.app.focus(self.sample_verbs)
        
    def provide_feedback_on_conjugation_results(self):
        """
        This method allows users to provide feedback on the conjugation results by adding a button next to each conjugated form.
        When the button is clicked, a prompt will appear for the user to enter their feedback.
        The feedback will be logged in a separate file for later analysis.
        """
        for form in self.conjugation_tables.children:
            feedback_button = form.add(textual.Button("Provide Feedback"))
            feedback_button.on_click(self.handle_feedback_submit)

    def handle_feedback_submit(self, form):
        """
        Handles the event when the user clicks the feedback button by displaying a prompt for the user to enter their feedback.
        The feedback is then logged in a separate file for later analysis.
        """
        feedback_prompt = form.add(textual.Prompt(placeholder="Enter your feedback"))
        feedback_prompt.on_submit(self.log_feedback)
        
    def log_feedback(self, feedback, form):
        """
        Logs the user's feedback in a separate file for later analysis.
        The feedback is associated with the conjugated form that the user provided feedback on.
        """
        with open("feedback.log", "a") as feedback_log:
            feedback_log.write("{} - {}\n".format(form, feedback))
            feedback_prompt.remove()
            form.add(textual.Text("Thank you for your feedback!"))
        
    def init_help_section(self):
        """
        Initialize the help section with instructions on how to use the TUI
        """
        self.help_section.add(textual.Text("Enter a verb in the prompt to conjugate it."))
        self.help_section.add(textual.Text("Use the export button to save the conjugations."))
        self.help_section.add(textual.Text("Use the language selector to choose the language for conjugation."))
        self.help_section.add(textual.Text("Use the subject selector to choose between abbrev or pronoun for conjugations"))
        self.help_section.add(textual.Text("Use the verb history section to view previous conjugations"))
        self.help_section.update()
        
    def run(self):
        """
        Start the TUI
        """
        self.app.run()
        
    def init(self):
        self.conjugation_history = {}
        self.init()
        
    def del(self):
        self.app.exit()


    
        
    




    
