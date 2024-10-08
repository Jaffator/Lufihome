from flask import Blueprint, render_template, url_for, redirect, request, flash
from modules import query
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, HiddenField, SelectField, TextAreaField, validators, FieldList, SelectMultipleField, widgets
from wtforms.validators import DataRequired
from markupsafe import Markup


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m  '
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


areas = Blueprint('areas', __name__)


class BootstrapListWidget(widgets.ListWidget):

    def __call__(self, field, **kwargs):
        kwargs.setdefault("id", field.id)
        html = [f"<{self.html_tag} {widgets.html_params(**kwargs)}>"]
        for subfield in field:
            if self.prefix_label:
                html.append(
                    f"<li class='list-group-item'>{subfield.label} {subfield(class_='form-check-input ms-1')}</li>")
            else:
                html.append(
                    f"<li class='list-group-item'>{subfield(class_='form-check-input me-1')} {subfield.label}</li>")
        html.append("</%s>" % self.html_tag)
        return Markup("".join(html))


class Sensors(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()


class AlarmArea(FlaskForm):
    name = StringField("Area Name:", validators=[DataRequired()])
    id = HiddenField()
    sensors = Sensors()
    # ('pokus', choices=[('1', 'ad'), ('2', 'sdfs'), ('3', 'sdf')])
    submit = SubmitField()


@ areas.route('/areas', methods=['GET', 'POST'])
def areas_page():
    sensors_names = query.get_AllSensorsNames()
    areas_dict = query.get_Areas(True)
    for i in range(len(areas_dict)):
        alarmArea = AlarmArea()
        alarmArea.name.data = areas_dict[i]['AreaName']
        alarmArea.id.data = areas_dict[i]['AreaID']
        alarmArea.sensors.choices = list(sensors_names)
        areas_dict[i].update({'alarmArea': alarmArea})
        areas_dict[i]['alarmArea'].sensors.data = query.get_sensorsNames_AreasDefition(
            areas_dict[i]['AreaName'])

    # print(areas_dict)

    newArea = AlarmArea()

    return render_template('areas.html', areas_dict=areas_dict, newArea=newArea)


@ areas.route('/areas/insert', methods=["POST"])
def insert():
    if request.method == "POST":
        newArea = AlarmArea()
        print("New Area: ", newArea.name.data, newArea.sensors.data)
        try:
            query.set_newArea(newArea.name.data, newArea.sensors.data)
        except:
            msg = "Something went wrong"
            cat = 'error'
        else:
            msg = "Area Inserted Succesfully"
            cat = 'message'
        print(msg, cat)
        flash(msg, cat)
        return redirect('/areas')


@ areas.route('/areas/update', methods=["GET", "POST"])
def update():
    if request.method == "POST":
        area = AlarmArea()
        print(
            f"Edited sensors:{bcolors.OKCYAN}{bcolors.BOLD}{area.sensors.data}{bcolors.ENDC}")
        print(
            f"Edited areaName: {bcolors.OKCYAN}{bcolors.BOLD}{area.name.data}{bcolors.ENDC} id:{bcolors.OKCYAN}{area.id.data}{bcolors.ENDC} ")
        areaDef = query.get_AreaDefiniton(True)
        for sensor in area.sensors.data:
            sensorID = query.get_sensorID_by_name(sensor)
            for item in areaDef:
                if (item['SensorID'] == sensorID) and (item['AreaID'] == area.id.data):
                    update = False
                else:
                    update = True

        # for item in request.form:
        #     print(item)

        # query.update_Area(area.name.data, area.id.data)
        return redirect('/areas')


@ areas.route('/areas/delete', methods=["GET", "POST"])
def delete():
    if request.method == "POST":
        nameID = request.form['areaID']
        print(nameID)
        try:
            query.delete_Area(nameID)
        except:
            msg = "Something went wrong"
            cat = 'error'
        else:
            msg = "Area Deleted Succesfully"
            cat = 'message'
        print(msg, cat)
        flash(msg, cat)
        return redirect('/areas')
