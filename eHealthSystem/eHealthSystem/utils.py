from .models import User

def generate_matric_id(account_type):
    role_prefix = {
        'STA': 'A24DW',  # Staff prefix
        'LEC': 'L24DW',  # Lecturer prefix
        'STU': 'S24DW',  # Student prefix
    }.get(account_type, 'S24DW')  # Default to 'S24DW' if no valid account type

    last_user = User.objects.filter(matric_id__startswith=role_prefix).order_by('-matric_id').first()

    if last_user:
        matric_id = f"{role_prefix}{str(int(last_user.matric_id[5:]) + 1).zfill(4)}"
    else:
        matric_id = f"{role_prefix}0001"  # If no users exist for that role, start with 0001

    return matric_id