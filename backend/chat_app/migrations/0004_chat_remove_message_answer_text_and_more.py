# Generated by Django 4.2.1 on 2023-08-18 11:34
import random, string
from django.contrib.auth import get_user_model
from django.db import migrations, models
import django.utils.timezone


def create_user(apps, schema_editor):
    User = get_user_model()
    user = User(id=100, username='GPT-3.5-turbo', email="",
                password=''.join(random.choice(string.ascii_letters) for _ in range(30)))
    user.save()


class Migration(migrations.Migration):
    dependencies = [
        ('user_app', '0003_rename_profile_agent'),
        ('chat_app', '0003_alter_message_answer_text_alter_message_message_text'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Dialog',
            new_name='Chat',
        ),
        migrations.AddField(
            model_name='chat',
            name='owner_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='owner_id',
                                    to='user_app.agent'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='chat',
            name='addressee_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='addressee_id',
                                    to='user_app.agent'),
            preserve_default=False,
        ),
        migrations.RunSQL('UPDATE chat_app_chat SET owner_id_id=user_id_id, addressee_id_id=user_id_id;'),
        migrations.RemoveField(
            model_name='chat',
            name='user_id',
        ),
        migrations.RenameField(
            model_name='message',
            old_name='dialog_id',
            new_name='chat_id'
        ),
        migrations.AddField(
            model_name='message',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='message',
            name='owner_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='user_app.agent'),
        ),
        # migrations.RunSQL('UPDATE chat_app_message SET owner_id_id=user_id_id, addressee_id_id=user_id_id;'),
        migrations.RunPython(create_user),
        migrations.RunSQL('UPDATE user_app_agent SET id=100 WHERE user_id_id=100'),
        migrations.RunSQL("""
            INSERT INTO chat_app_message (message_text, chat_id_id, created_at, owner_id_id)
            SELECT answer_text, chat_id_id, created_at, 100
            FROM chat_app_message
            WHERE answer_text IS NOT NULL;            
            """),
        migrations.RunSQL("""
            CREATE TABLE temp_table AS SELECT * FROM chat_app_message;
            UPDATE temp_table SET id = id * 2;
            DELETE FROM chat_app_message;
            INSERT INTO chat_app_message SELECT * FROM temp_table;
            DROP TABLE temp_table;
        """),
        migrations.RunSQL("""
                CREATE TABLE temp_table AS SELECT * FROM chat_app_message;
                UPDATE temp_table
                SET id = id - (SELECT COUNT(*) FROM temp_table) + 1 
                WHERE ID > (SELECT MAX(id)/2 FROM temp_table);
                DELETE FROM chat_app_message;
                INSERT INTO chat_app_message SELECT * FROM temp_table;
                DROP TABLE temp_table;
        """),
        migrations.RemoveField(
            model_name='message',
            name='answer_text',
        ),
    ]
