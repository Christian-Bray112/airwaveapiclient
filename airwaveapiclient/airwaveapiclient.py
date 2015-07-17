# -*- coding: utf-8 -*-

"""airwaveapiclient."""


import requests
import os
import xmltodict
from collections import OrderedDict


class AirWaveAPIClient(object):

    """Aruba networks AirWave API client.

    Attributes:

        :username (str): Login username.
        :password (str): Login password.
        :address (str): Host name or ip address.
        :session (requests.sessions.Session): Session for connection pooling.

    """

    def __init__(self, **kwargs):
        """Initialize AirWaveAPIClient.

        Args:

            :username (str): Login username.
            :password (str): Login password.
            :address (str): Host name or ip address.

        Usage: ::

            >>> from airwaveapiclient import AirWaveAPIClient
            >>> airwave = AirWaveAPIClient(username='admin',
            >>>                            password='xxxxx',
            >>>                            address='192.168.1.1')
            >>>


        """
        self.username = kwargs['username']
        self.password = kwargs['password']
        self.address = kwargs['address']
        self.session = None

    def login(self):
        """Login to AirWave.

        Returns:

            requests.models.Response

        Usage: ::

            >>> res = airwave.login()
            >>> res.status_code
            200

        """
        requests.packages.urllib3.disable_warnings()
        self.session = requests.Session()
        url = 'https://%s/LOGIN' % self.address
        destination = '/'
        next_action = ''
        params = {'credential_0': self.username,
                  'credential_1': self.password,
                  'login': 'Log In',
                  'destination': destination,
                  'next_action': next_action}
        return self.session.post(url, params=params, verify=False)

    def logout(self):
        """Logout.

        Close the session.

        Usage: ::

            >>> airwave.logout()

        """
        self.session.close()

    def api_path(self, path):
        """API URL.

        Args:

            :path (str): Path for API URL.

        Returns:

            URL string 'https://xxx.xxx.xxx.xxx/xxxxxx'

        """
        url = 'https://%s/' % self.address
        return os.path.join(url, path)

    def ap_list(self, ap_ids=None):
        """Get Access Point list.

        Args:

            :ap_ids (optional[list]): You may specify multiple
                Access Point IDs. Default is None.

        Returns:

            :Response: requests.models.Response.

        Usage: ::

            # Get all Acces Point.

            >>> res = airwave.ap_list()
            >>> res.url
            'https://192.168.1.1/ap_list.xml'

            # Get specified Acces Point.

            >>> res = airwave.ap_list([123, 124, 125])
            >>> res.status_code
            200
            >>> res.url
            'https://192.168.1.1/ap_list.xml?id=123&id=124&id=125'
            >>> res.text  # xml output.
            '<?xml version="1.0" encoding="utf-8" ...'

        """
        url = self.api_path('ap_list.xml')
        if ap_ids:
            params = AirWaveAPIClient.id_params(ap_ids)
            return self.session.get(url, verify=False, params=params)
        return self.session.get(url, verify=False)

    def ap_detail(self, ap_id):
        """Get Access Point detail inforamtion.

        Args:

            :ap_id (int): Access Point ID.

        Returns:

            :Response: requests.models.Response.

        Usage: ::

            >>> res = airwave.ap_detail(123)
            >>> res.status_code
            200
            >>> res.url
            'https://192.168.1.1/ap_detail.xml?id=123'
            >>> res.text  # xml output.
            '<?xml version="1.0" encoding="utf-8" ...'

        """
        url = self.api_path('ap_detail.xml')
        params = {'id': ap_id}
        params = AirWaveAPIClient.urlencode(params)
        return self.session.get(url, verify=False, params=params)

    def client_detail(self, mac):
        """Client detail inforamtion.

        Args:

            :mac (str): Client device's MAC address.

        Returns:

            :Response: requests.models.Response.

        Usage: ::

            >>> res = airwave.client_detail('12:34:56:78:90:AB')
            >>> res.status_code
            200
            >>> res.url
            'https://192.168.1.1/client_detail.xml?mac=12%3A34%3A56%3A78%3A90%3AAB'
            >>> res.text  # xml output.
            '<?xml version="1.0" encoding="utf-8" ...'

        """
        url = self.api_path('client_detail.xml')
        params = {'mac': mac}
        params = AirWaveAPIClient.urlencode(params)
        return self.session.get(url, verify=False, params=params)

    def rogue_detail(self, ap_id):
        """Rogue detail inforamtion.

        Args:

            :ap_id (int): Access Point ID.

        Returns:

            :Response: requests.models.Response.

        Usage: ::

            >>> res = airwave.rogue_detail(123)
            >>> res.status_code
            200
            >>> res.text  # xml output.
            '<?xml version="1.0" encoding="utf-8" ...'

        """
        url = self.api_path('rogue_detail.xml')
        params = {'id': ap_id}
        params = AirWaveAPIClient.urlencode(params)
        return self.session.get(url, verify=False, params=params)

    def report_list(self, reports_search_title=None):
        """Report list inforamtion.

        .. warning::

            This method result includes API output that is XHTML(not XML).

        Args:

            :reports_search_title (optional[str]): You may filter with
                report title.  Default is None.

        Returns:

            :Response: requests.models.Response.

        Usage: ::

            # Get report list.

            >>> res = airwave.report_list()
            >>> res.url
            'https://192.168.1.1/nf/reports_list?format=xml'

            # Get specified report list with title.

            >>> res = airwave.report_list('Weekly Report')
            >>> res.status_code
            200
            >>> res.url
            'https://192.168.1.1/nf/reports_list?reports_search_title=Weekly+Report&format=xml'
            >>> res.text  # xhtml output.
            '<?xml version="1.0"?><!DOCTYPE html ...'

        """
        url = self.api_path('nf/reports_list')
        params = {'format': 'xml'}
        if reports_search_title:
            params['reports_search_title'] = reports_search_title
        params = AirWaveAPIClient.urlencode(params)
        return self.session.get(url, verify=False, params=params)

    def report_detail(self, report_id):
        """Report detail inforamtion.

        .. warning::

            This method result includes API output that is XHTML(not XML).

        Args:

            :report_id (int): Report ID.

        Returns:

            :Response: requests.models.Response.

        Usage: ::

            >>> res = airwave.report_detail(123)
            >>> res.status_code
            200
            >>> res.url
            'https://192.1681.1/nf/report_detail?id=123&format=xml'
            >>> res.text  # xhtml output.
            '<?xml version="1.0"?><!DOCTYPE html ...'

        """
        url = self.api_path('nf/report_detail')
        params = {'id': report_id, 'format': 'xml'}
        params = AirWaveAPIClient.urlencode(params)
        return self.session.get(url, verify=False, params=params)

    def __graph_url(self, params):
        """RRD Graph URL."""
        url = self.api_path('nf/rrd_graph')
        params['start'] = '-%ss' % params['start']
        params['end'] = '-%ss' % params['end']
        params = AirWaveAPIClient.urlencode(params)
        return '%s?%s' % (url, params)

    def ap_base_url(self, graph_type, **kwargs):
        """RRD Graph Base URL for Access Point.

        Args :

            graph_type (str): Graph Type.

        Keyword Args :

            :ap_id (int): Access Point ID.
            :radio_index (int): Access Point Radio type index.
            :start (int): Graph start time.
                Seconds of current time difference.
                1 hour ago is 3600.
                2 hours ago is 7200.
                3 days ago is 259200(3600sec x 24H x 3days).
            :end (int, optional): Graph end time.
                Seconds of current time difference.
                Default is 0.

        Returns:

            :str: Graph URL string.

        """

        params = {'id': kwargs['ap_id'],
                  'radio_index': kwargs['radio_index'],
                  'start': kwargs['start'],
                  'end': kwargs.get('end', 0),
                  'type': graph_type}
        return self.__graph_url(params)

    def ap_client_count_graph_url(self, **kwargs):
        """RRD Graph URL for Access Point Client Count.

        Keyword Args:

            :ap_id (int): Access Point ID.
            :radio_index (int): Access Point Radio type index.
            :start (int): Graph start time(seconds ago).
            :end (int, optional): Graph end time(seconds ago). Default is 0.

        Returns:

            :str: Graph URL string.

        Usage: ::

            >>> airwave.ap_client_count_graph_url(ap_id=1,
            ...                                   radio_index=1,
            ...                                   start=3600)
            'https://x.x.x.x/nf/rrd_graph?
                end=-0s&id=1&radio_index=1&start=-3600s&type=ap_client_count'

        """
        return self.ap_base_url('ap_client_count', **kwargs)

    def ap_bandwidth_graph_url(self, **kwargs):
        """RRD Graph URL for Access Point Bandwidth.

        Keyword Args :

            :ap_id (int): Access Point ID.
            :radio_index (int): Access Point Radio type index.
            :start (int): Graph start time(seconds ago).
            :end (int, optional): Graph end time(seconds ago). Default is 0.

        Returns:

            :str: Graph URL string.

        Usage: ::

            >>> airwave.ap_bandwidth_graph_url(ap_id=1,
            ...                                radio_index=1,
            ...                                start=3600)
            'https://x.x.x.x/nf/rrd_graph?
                end=-0s&id=1&radio_index=1&start=-3600s&type=ap_bandwidth'


        """
        return self.ap_base_url('ap_bandwidth', **kwargs)

    def dot11_counters_graph_url(self, **kwargs):
        """RRD Graph URL for 802.11 Counters.

        Keyword Args :

            :ap_id (int): Access Point ID.
            :radio_index (int): Access Point Radio type index.
            :start (int): Graph start time(seconds ago).
            :end (int, optional): Graph end time(seconds ago). Default is 0.

        Returns:

            :str: Graph URL string.

        Usage: ::

            >>> airwave.dot11_counters_graph_url(ap_id=1,
            ...                                  radio_index=1,
            ...                                  start=3600)
            'https://x.x.x.x/nf/rrd_graph?
                end=-0s&id=1&radio_index=1&start=-3600s&type=dot11_counters'

        """

        return self.ap_base_url('dot11_counters', **kwargs)

    def radio_base_url(self, graph_type, **kwargs):
        """RRD Graph URL for Radio Base.

        Args :

            graph_type (str): Graph Type.

        Keyword Args :

            :ap_uid (str): Access Point UID.
            :radio_index (int): Access Point Radio type index.
            :radio_interface (int): Radio Interface.
            :graph_type (str): Graph type name.
            :start (int): Graph start time.
                Seconds of current time difference.
                1 hour ago is 3600.
                2 hours ago is 7200.
                3 days ago is 259200(3600sec x 24H x 3days).
            :end (int, optional): Graph end time.
                Seconds of current time difference.
                Default is 0.

        Returns:

            :str: Graph URL string.


        """

        params = {'ap_uid': kwargs['ap_uid'],
                  'radio_index': kwargs['radio_index'],
                  'radio_interface': kwargs['radio_interface'],
                  'start': kwargs['start'],
                  'end': kwargs.get('end', 0),
                  'type': graph_type}
        return self.__graph_url(params)

    def radio_channel_graph_url(self, **kwargs):
        """RRD Graph URL for Radio Channel.

        Keyword Args :

            :ap_uid (str): Access Point UID.
            :radio_index (int): Access Point Radio type index.
            :radio_interface (int): Radio Interface.
            :start (int): Graph start time(seconds ago).
            :end (int, optional): Graph end time(seconds ago). Default is 0.

        Returns:

            :str: Graph URL string.

        Usage: ::

            >>> airwave.radio_channel_graph_url(ap_uid="01:23:45:67:89:AB",
            ...                                 radio_index=1,
            ...                                 radio_interface=1,
            ...                                 start=3600)
            'https://10.129.2.220/nf/rrd_graph?
                ap_uid=01%3A23%3A45%3A67%3A89%3AAB
                &end=-0s
                &radio_index=1
                &radio_interface=1
                &start=-3600s
                &type=radio_channel'

        """

        return self.radio_base_url('radio_channel', **kwargs)

    def radio_noise_graph_url(self, **kwargs):
        """RRD Graph URL for Radio Noise.

        Keyword Args :

            :ap_uid (str): Access Point UID.
            :radio_index (int): Access Point Radio type index.
            :radio_interface (int): Radio Interface.
            :start (int): Graph start time(seconds ago).
            :end (int, optional): Graph end time(seconds ago). Default is 0.

        Returns:

            :str: Graph URL string.

        Usage: ::

            >>> airwave.radio_noise_graph_url(ap_uid="01:23:45:67:89:AB",
            ...                               radio_index=1,
            ...                               radio_interface=1,
            ...                               start=3600)
            'https://x.x.x.x/nf/rrd_graph?
                ap_uid=01%3A23%3A45%3A67%3A89%3AAB
                &end=-0s
                &radio_index=1
                &radio_interface=1
                &start=-3600s
                &type=radio_noise'

        """

        return self.radio_base_url('radio_noise', **kwargs)

    def radio_power_graph_url(self, **kwargs):
        """RRD Graph URL for Radio Power.

        Keyword Args :

            :ap_uid (str): Access Point UID.
            :radio_index (int): Access Point Radio type index.
            :radio_interface (int): Radio Interface.
            :start (int): Graph start time(seconds ago).
            :end (int, optional): Graph end time(seconds ago). Default is 0.

        Returns:

            :str: Graph URL string.

        Usage: ::

            >>> airwave.radio_power_graph_url(ap_uid="01:23:45:67:89:AB",
            ...                               radio_index=1,
            ...                               radio_interface=1,
            ...                               start=3600)
            'https://x.x.x.x/nf/rrd_graph?
                ap_uid=01%3A23%3A45%3A67%3A89%3AAB
                &end=-0s
                &radio_index=1
                &radio_interface=1
                &start=-3600s
                &type=radio_power'

        """

        return self.radio_base_url('radio_power', **kwargs)

    def radio_errors_graph_url(self, **kwargs):
        """RRD Graph URL for Radio Errors.

        Keyword Args :

            :ap_uid (str): Access Point UID.
            :radio_index (int): Access Point Radio type index.
            :radio_interface (int): Radio Interface.
            :start (int): Graph start time(seconds ago).
            :end (int, optional): Graph end time(seconds ago). Default is 0.

        Returns:

            :str: Graph URL string.

        Usage: ::

            >>> airwave.radio_errors_graph_url(ap_uid="01:23:45:67:89:AB",
            ...                                radio_index=1,
            ...                                radio_interface=1,
            ...                                start=3600)
            'https://x.x.x.x/nf/rrd_graph?
                ap_uid=01%3A23%3A45%3A67%3A89%3AAB
                &end=-0s
                &radio_index=1
                &radio_interface=1
                &start=-3600s
                &type=radio_errors'

        """

        return self.radio_base_url('radio_errors', **kwargs)

    def radio_goodput_graph_url(self, **kwargs):
        """RRD Graph URL for Radio GoodPut.

        Keyword Args :

            :ap_uid (str): Access Point UID.
            :radio_index (int): Access Point Radio type index.
            :radio_interface (int): Radio Interface.
            :start (int): Graph start time(seconds ago).
            :end (int, optional): Graph end time(seconds ago). Default is 0.

        Returns:

            :str: Graph URL string.

        Usage: ::

            >>> airwave.radio_goodput_graph_url(ap_uid="01:23:45:67:89:AB",
            ...                                 radio_index=1,
            ...                                 radio_interface=1,
            ...                                 start=3600)
            'https://x.x.x.x/nf/rrd_graph?
                ap_uid=01%3A23%3A45%3A67%3A89%3AAB
                &end=-0s
                &radio_index=1
                &radio_interface=1
                &start=-3600s
                &type=radio_goodput'

        """

        return self.radio_base_url('radio_goodput', **kwargs)

    def channel_utilization_graph_url(self, **kwargs):
        """RRD Graph URL for Channel utilization.

        Keyword Args :

            :ap_uid (str): Access Point UID.
            :radio_index (int): Access Point Radio type index.
            :radio_interface (int): Radio Interface.
            :start (int): Graph start time(seconds ago).
            :end (int, optional): Graph end time(seconds ago). Default is 0.

        Returns:

            :str: Graph URL string.

        Usage: ::

            >>> airwave.channel_utilization_graph_url(
            ...     ap_uid="01:23:45:67:89:AB",
            ...     radio_index=1,
            ...     radio_interface=1,
            ...     start=3600)
            'https://x.x.x.x/nf/rrd_graph?
                ap_uid=01%3A23%3A45%3A67%3A89%3AAB
                &end=-0s
                &radio_index=1
                &radio_interface=1
                &start=-3600s
                &type=channel_utilization'

        """

        return self.radio_base_url('channel_utilization', **kwargs)

    @staticmethod
    def id_params(ap_ids):
        """Make access point id string."""
        return '&'.join(["id=%s" % ap_id for ap_id in ap_ids])

    @staticmethod
    def urlencode(params):
        """URL Encode."""
        params = sorted(params.items())
        return requests.packages.urllib3.request.urlencode(params)


class APList(list):

    """class APList.

    Access Point List.

    """

    def __init__(self, xml):
        """Constructor."""
        data = xmltodict.parse(xml)
        obj = data['amp:amp_ap_list']['ap']
        list.__init__(self, obj)

    def search(self, obj):
        """Search Access Point."""
        if isinstance(obj, int):
            for node in self:
                if int(node['@id']) == obj:
                    return node

        if isinstance(obj, str):
            for node in self:
                if node['name'] == obj:
                    return node
        return None


class APDetail(OrderedDict):

    """class APDetail.

    Access Point Detail.

    """
    def __init__(self, xml):
        """Constructor."""
        data = xmltodict.parse(xml)
        obj = data['amp:amp_ap_detail']['ap']
        OrderedDict.__init__(self, obj)
