__author__ = 'ivanbahdanau'
import web

import FileUtils as FileUtils


urls = (
    '/(.*)', 'CopterController'
)
app = web.application(urls, globals())


class CopterController(object):
    def check_for_key_and_return(self, key_value, default_value):
        if web.input().has_key(key_value):
            is_on = web.input()[key_value]
        else:
            is_on = default_value
        return is_on

    def GET(self, name):
        if len(web.input().items()) == 0:
            return "No parameters"
        (copter_is_on, copter_torque, is_kill, control_force) = FileUtils.read_file_data()
        is_on = self.check_for_key_and_return('is_on', copter_is_on)
        torque = self.check_for_key_and_return('copter_torque', copter_torque)
        is_kill = self.check_for_key_and_return('kill', is_kill)
        control_force = self.check_for_key_and_return('control_force', control_force)
        if is_on != None and torque != None and is_kill != None:
            FileUtils.write_file_data(is_on, torque, is_kill, control_force)
            print (is_on, torque, is_kill, control_force)
            return "ACK"
        else:
            return "Failed"


if __name__ == "__main__":
    app.run()