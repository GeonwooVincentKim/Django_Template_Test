from django import forms


# If execute this code on the Python Shell Commander
# basically, Django provide programmers <label> tag
# for the accessibility.

# And It has a built-in output System.
# Such as <ul(but it prints li)>, <p> tags.

# Also it can shows HTML related to Specification Field.
# Such as variable['name of DataBase Field']

# And it makes bound form if connect to the Form Instance.
# Call is_valid() Method that connected Form to check
# Whether Validates the Data.
class ContactForm(forms.Form):
    subject = forms.CharField(max_length=100)
    # Email Field is not required.
    email = forms.EmailField(required=False,
                             label='Your e-mail address')
    # But Message Field and Subject Field are required.
    # Form Framework separates each Fields of Expression logic
    # to the Widget Set.
    message = forms.CharField(widget=forms.Textarea)

    def clean_message(self):
        message = self.cleaned_data['message']
        num_words = len(message.split())

        if num_words < 4:
            raise forms.ValidationError("Not Enough words!")
        return message

# If Forms Instance that the Data is confirmed Valid,
# It can use cleaned_data Attribute
