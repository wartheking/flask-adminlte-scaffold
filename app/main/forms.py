from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, PasswordField, SelectField, TextAreaField, HiddenField
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo


class FurnituresDataForm(FlaskForm):
    furnitureID = StringField('家具ID', validators=[DataRequired(message='不能为空'), Length(0, 64, message='长度不正确')])
    # furnitureTpye = SelectField('通知类型', choices=[('MAIL', '邮件通知'), ('SMS', '短信通知')],
    #                           validators=[DataRequired(message='不能为空'), Length(0, 64, message='长度不正确')])
    uploadUserID = StringField('上传用户ID', validators=[DataRequired(message='不能为空'), Length(0, 64, message='长度不正确')])
    organization = StringField('上传组织', validators=[DataRequired(message='不能为空'), Length(0, 64, message='长度不正确')])
    furnitureType = StringField('家具类型1', validators=[DataRequired(message='不能为空'), Length(0, 64, message='长度不正确')])
    furnitureType2 = StringField('家具类型2', validators=[DataRequired(message='不能为空'), Length(0, 64, message='长度不正确')])
    furniturePicUrl = StringField('缩略图', validators=[DataRequired(message='不能为空'), Length(0, 64, message='长度不正确')])
    #uploadUserID = BooleanField('生效标识', default=True)
    submit = SubmitField('提交')


