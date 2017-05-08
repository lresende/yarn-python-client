# -*- coding: utf-8 -*-

from pprint import pprint
from unittest import TestCase
from yarn_api_client.resource_manager import ResourceManager
from yarn_api_client.errors import IllegalArgumentError

class ResourceManagerTestCase(TestCase):
    def setUp(self):
        self.resourceManager = ResourceManager(serviceEndpoint='https://lresende-iop-cluster:8443/gateway/default/resourcemanager/v1/cluster',
                                  username='guest',
                                  password='guest-password')
        self.resourceManagerHttp = ResourceManager(serviceEndpoint='http://lresende-iop-cluster:8088/ws/v1/cluster')


    def test_cluster_information(self):
        info = self.resourceManager.cluster_information()
        pprint(info.data)
        self.assertEqual(info.data['clusterInfo']['state'], 'STARTED')



    def test_cluster_metrics(self):
        metrics = self.resourceManager.cluster_metrics()
        pprint(metrics.data)
        self.assertGreater(metrics.data['clusterMetrics']['activeNodes'], 0)
        self.assertIsNotNone(metrics.data['clusterMetrics']['totalNodes'])


    def test_cluster_scheduler(self):
        scheduler = self.resourceManager.cluster_scheduler()
        pprint(scheduler.data)
        self.assertIsNotNone(scheduler.data['scheduler']['schedulerInfo'])


    def test_cluster_applications(self):
        apps = self.resourceManager.cluster_applications()
        pprint(apps.data)
        self.assertIsNotNone(apps.data['apps'])

    def test_cluster_application_statistics(self):
        appstats = self.resourceManager.cluster_application_statistics()
        pprint(appstats.data)
        self.assertIsNotNone(appstats.data['appStatInfo'])
        # TODO: test arguments

    def test_cluster_nodes(self):
        nodes = self.resourceManager.cluster_nodes()
        pprint(nodes.data)
        self.assertIsNotNone(nodes.data['nodes'])

        running_nodes = self.resourceManager.cluster_nodes(state='RUNNING', healthy='true')
        pprint(running_nodes.data)
        self.assertIsNotNone(nodes.data['nodes'])

        running_nodes = self.resourceManager.cluster_nodes(state='NEW')
        pprint(running_nodes.data)
        self.assertIsNone(nodes.data['nodes'])

    def test_query_am_host(self):
        data = self.resourceManagerHttp.cluster_applications(user='hive').data
        self.assertIsNotNone(data['apps'])
        for app in data['apps']['app']:
            if app['name'] == 'Thrift JDBC/ODBC Server':
                pprint(app['amHostHttpAddress'])
                pprint(app['id'])
                self.assertIsNotNone(app['amHostHttpAddress'])
                self.assertIsNotNone(app['id'])
                self.assertEqual(app['state'], 'RUNNING')
