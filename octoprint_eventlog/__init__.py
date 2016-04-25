# coding=utf-8
from __future__ import absolute_import

### (Don't forget to remove me)
# This is a basic skeleton for your plugin's __init__.py. You probably want to adjust the class name of your plugin
# as well as the plugin mixins it's subclassing from. This is really just a basic skeleton to get you started,
# defining your plugin as a template plugin, settings and asset plugin. Feel free to add or remove mixins
# as necessary.
#
# Take a look at the documentation on what other plugin mixins are available.

import octoprint.plugin

class EventlogPlugin(octoprint.plugin.SettingsPlugin,
                     octoprint.plugin.AssetPlugin,
		     octoprint.plugin.StartupPlugin,
		     octoprint.plugin.ShutdownPlugin,
		     octoprint.plugin.EventHandlerPlugin,
                     octoprint.plugin.TemplatePlugin):

	def on_after_startup():
		db = MySQLdb.connect(host="192.168.0.182",user="tools",passwd="tools",db="tools")
		cur = db.cursor()

	def on_shutdown():
		cur.close()
		db.close()

	##~~ EventHandlerPlugin mixin
	def on_event(event, payload):
		cur.execute("INSERT INTO robo_events (event, payload) VALUES (%s, %s)", (event, payload))

	##~~ SettingsPlugin mixin

	def get_settings_defaults(self):
		return dict(
			# put your plugin's default settings here
		)

	##~~ AssetPlugin mixin

	def get_assets(self):
		# Define your plugin's asset files to automatically include in the
		# core UI here.
		return dict(
			js=["js/eventlog.js"],
			css=["css/eventlog.css"],
			less=["less/eventlog.less"]
		)

	##~~ Softwareupdate hook

	def get_update_information(self):
		# Define the configuration for your plugin to use with the Software Update
		# Plugin here. See https://github.com/foosel/OctoPrint/wiki/Plugin:-Software-Update
		# for details.
		return dict(
			eventlog=dict(
				displayName="Eventlog Plugin",
				displayVersion=self._plugin_version,

				# version check: github repository
				type="github_release",
				user="BrandoCommando",
				repo="OctoPrint-EventLog",
				current=self._plugin_version,

				# update method: pip
				pip="https://github.com/BrandoCommando/OctoPrint-EventLog/archive/{target_version}.zip"
			)
		)


# If you want your plugin to be registered within OctoPrint under a different name than what you defined in setup.py
# ("OctoPrint-PluginSkeleton"), you may define that here. Same goes for the other metadata derived from setup.py that
# can be overwritten via __plugin_xyz__ control properties. See the documentation for that.
__plugin_name__ = "Eventlog Plugin"

def __plugin_load__():
	global __plugin_implementation__
	__plugin_implementation__ = EventlogPlugin()

	global __plugin_hooks__
	__plugin_hooks__ = {
		"octoprint.plugin.softwareupdate.check_config": __plugin_implementation__.get_update_information
	}

