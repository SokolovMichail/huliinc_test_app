from django.contrib.auth import get_user_model


class ReportGenerator():

    @staticmethod
    def generate_report():
        User = get_user_model()
        print(len(User.objects.all()))
        # with open("x.txt",'w') as f:
        #     f.write(str(len(User.objects.all())))