from flask_wtf import FlaskForm
from wtforms import StringField,FloatField, SubmitField, BooleanField, PasswordField, SelectField, TextAreaField, HiddenField
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo

tempChoices = {}
furnitureType2_updated = False
class FurnituresDataForm(FlaskForm):
    
    
    furnitureID = StringField('家具ID', validators=[DataRequired(message='不能为空'), Length(0, 64, message='长度不正确')])
    # furnitureTpye = SelectField('通知类型', choices=[('MAIL', '邮件通知'), ('SMS', '短信通知')],
    #                           validators=[DataRequired(message='不能为空'), Length(0, 64, message='长度不正确')])
    uploadUserID = StringField('上传用户ID', validators=[DataRequired(message='不能为空'), Length(0, 64, message='长度不正确')])
    organization = StringField('上传供应商', validators=[DataRequired(message='不能为空'), Length(0, 64, message='长度不正确')])
    #furniturePicUrl = HiddenField('家具图片URL', validators=[DataRequired(message='不能为空'), Length(0, 255, message='长度不正确')])
    furnitureType = SelectField('家具类型1', choices=[('0', '门'), ('1', '窗'),('5', '椅凳')],validators=[DataRequired(message='不能为空'), Length(0, 64, message='长度不正确')])
    furnitureType2 = SelectField('家具类型2', choices=[("0.00", '未分类'), ("0.01", '室内门'),("0.02", '推拉门')],validators=[DataRequired(message='不能为空'), Length(0, 64, message='长度不正确')])
    #furnitureType2 = StringField('家具类型2',validators=[DataRequired(message='不能为空'), Length(0, 64, message='长度不正确')])
    #uploadUserID = BooleanField('生效标识', default=True)
    submit = SubmitField('提交')

    def __init__(self, furnitureTypeDic,furnitureTypeDic2, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.furnitureType.choices = list(furnitureTypeDic.items())
        self.furnitureType2.choices = list(furnitureTypeDic2.items())

    def update_furnitureType2_choices(self, choices):
        global tempChoices
        tempChoices = list(choices.items())
        global furnitureType2_updated
        furnitureType2_updated = True  # 标记为已更新

    def validate_on_submit(self):

        global tempChoices
        global furnitureType2_updated
        # 如果选择字段的选项已更新，重新设置选项
        if furnitureType2_updated:
            furnitureType2_updated = False
            self.furnitureType2.choices = tempChoices
        # 首先检查父类的验证结果
        if not super().validate_on_submit():
            return False

        return True