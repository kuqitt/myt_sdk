#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MYT API客户端测试
"""

import pytest
import requests

try:
    import requests_mock
except ImportError:
    requests_mock = None
from unittest.mock import patch

from py_myt.api_client import MYTAPIClient, create_client
from py_myt.exceptions import MYTSDKError

# 定义HAS_REQUESTS_MOCK常量
HAS_REQUESTS_MOCK = requests_mock is not None


@pytest.fixture
def setup_has_requests_mock():
    """设置requests_mock可用性"""
    return HAS_REQUESTS_MOCK


@pytest.mark.skipif(requests_mock is None, reason="requests_mock not installed")
class TestMYTAPIClient:
    """MYT API客户端测试类"""

    def setup_method(self):
        """测试前准备"""
        self.base_url = "http://127.0.0.1:5000"
        self.client = MYTAPIClient(base_url=self.base_url)

    def teardown_method(self):
        """测试后清理"""
        self.client.close()

    def test_init(self):
        """测试客户端初始化"""
        assert self.client.base_url == self.base_url
        assert self.client.timeout == 30
        assert self.client.session is not None

    def test_create_client(self):
        """测试便捷创建函数"""
        client = create_client()
        assert isinstance(client, MYTAPIClient)
        assert client.base_url == "http://127.0.0.1:5000"
        client.close()

    def test_get_version_success(self, requests_mock):
        """测试获取版本信息成功"""
        expected_response = {"code": 200, "data": "1.0.14.30.25", "message": ""}

        requests_mock.get(f"{self.base_url}/version", json=expected_response)

        result = self.client.get_version()
        assert result == expected_response
        assert result["data"] == "1.0.14.30.25"

    def test_login_success(self, requests_mock):
        """测试登录成功"""
        username = "admin"
        password = "password123"
        expected_response = {"code": 200, "msg": "5b7b1487fc2f659ae1cb748b5e937b0f"}

        requests_mock.get(
            f"{self.base_url}/login/{username}/{password}", json=expected_response
        )

        result = self.client.login(username, password)
        assert result == expected_response
        assert "msg" in result

    def test_query_myt_devices_success(self, requests_mock):
        """测试查询设备列表成功"""
        expected_response = {
            "code": 200,
            "message": "success",
            "data": {"192.168.181.27": "e5ef14d8cee888ae8a5e511d79d71593d"},
        }

        requests_mock.get(
            f"{self.base_url}/host_api/v1/query_myt", json=expected_response
        )

        result = self.client.query_myt_devices()
        assert result == expected_response
        assert "192.168.181.27" in result["data"]

    def test_get_image_list_v2_success(self, requests_mock):
        """测试获取镜像列表V2成功"""
        image_type = "p1"
        expected_response = {
            "code": 200,
            "msg": [
                {
                    "id": "46",
                    "image": "registry.cn-hangzhou.aliyuncs.com/whsyf/dobox:rk3588-dm-base-20230807-01",
                    "name": "test_0807",
                }
            ],
        }

        requests_mock.get(
            f"{self.base_url}/host_api/v1/get_img_list", json=expected_response
        )

        result = self.client.get_image_list_v2(image_type)
        assert result == expected_response
        assert len(result["msg"]) == 1

    def test_get_image_list_v2_invalid_type(self):
        """测试获取镜像列表V2无效类型"""
        with pytest.raises(MYTSDKError) as exc_info:
            self.client.get_image_list_v2("invalid_type")

        assert "无效的镜像类型" in str(exc_info.value)

    def test_get_image_list_v1_success(self, requests_mock):
        """测试获取镜像列表V1成功"""
        expected_response = {
            "code": 200,
            "msg": [
                {
                    "id": "49",
                    "image": "registry.cn-hangzhou.aliyuncs.com/whsyf/dobox:rk3588-dm-base-20230907-01",
                    "name": "test_beta_0907_1",
                }
            ],
        }

        requests_mock.get(f"{self.base_url}/get_img_list", json=expected_response)

        result = self.client.get_image_list_v1()
        assert result == expected_response

    def test_get_device_info_success(self, requests_mock):
        """测试获取机型信息成功"""
        expected_response = {"code": 200, "msg": {"HONOR": {"AKA-AL10": 39}}}

        requests_mock.get(f"{self.base_url}/get_devinfo", json=expected_response)

        result = self.client.get_device_info()
        assert result == expected_response
        assert "HONOR" in result["msg"]

    def test_connection_error(self, requests_mock):
        """测试连接错误"""
        requests_mock.get(
            f"{self.base_url}/version", exc=requests.exceptions.ConnectionError
        )

        with pytest.raises(MYTSDKError) as exc_info:
            self.client.get_version()

        assert "连接失败" in str(exc_info.value)

    def test_timeout_error(self, requests_mock):
        """测试超时错误"""
        requests_mock.get(f"{self.base_url}/version", exc=requests.exceptions.Timeout)

        with pytest.raises(MYTSDKError) as exc_info:
            self.client.get_version()

        assert "请求超时" in str(exc_info.value)

    def test_http_error(self, requests_mock):
        """测试HTTP错误"""
        requests_mock.get(f"{self.base_url}/version", status_code=404)

        with pytest.raises(MYTSDKError) as exc_info:
            self.client.get_version()

        assert "HTTP错误 404" in str(exc_info.value)

    def test_invalid_json_response(self, requests_mock):
        """测试无效JSON响应"""
        requests_mock.get(f"{self.base_url}/version", text="invalid json")

        with pytest.raises(MYTSDKError) as exc_info:
            self.client.get_version()

        assert "不是有效的JSON格式" in str(exc_info.value)

    def test_context_manager(self):
        """测试上下文管理器"""
        with create_client() as client:
            assert isinstance(client, MYTAPIClient)
        # 客户端应该已经关闭

    @pytest.mark.skipif(not HAS_REQUESTS_MOCK, reason="requests_mock not available")
    def test_create_android_container_basic(self, requests_mock):
        """测试基础容器创建"""
        # 模拟成功响应
        requests_mock.post(
            f"{self.base_url}/create/192.168.1.100/1/test_container",
            json={
                "code": 200,
                "msg": "容器创建成功",
                "data": {"container_id": "test_123"},
            },
        )

        result = self.client.create_android_container(
            ip="192.168.1.100", index=1, name="test_container"
        )

        assert result["code"] == 200
        assert "容器创建成功" in result["msg"]

    @pytest.mark.skipif(not HAS_REQUESTS_MOCK, reason="requests_mock not available")
    def test_create_android_container_advanced(self, requests_mock):
        """测试高级配置容器创建"""
        # 模拟成功响应
        requests_mock.post(
            f"{self.base_url}/create/192.168.1.100/2/advanced_container",
            json={"code": 200, "msg": "高级容器创建成功"},
        )

        result = self.client.create_android_container(
            ip="192.168.1.100",
            index=2,
            name="advanced_container",
            memory=2048,
            cpu="0,1,2,3",
            resolution=1,
            width=1080,
            height=1920,
            dpi=480,
            fps=60,
            sandbox=1,
            sandbox_size=32,
            tcp_map_port="{5555:55555}",
            adbport=5555,
        )

        assert result["code"] == 200

        # 验证请求参数
        last_request = requests_mock.last_request
        assert "memory=2048" in last_request.url
        assert "cpu=0%2C1%2C2%2C3" in last_request.url  # URL编码的逗号
        assert "resolution=1" in last_request.url
        assert "sandbox=1" in last_request.url

    @pytest.mark.skipif(not HAS_REQUESTS_MOCK, reason="requests_mock not available")
    def test_create_android_container_bridge_mode(self, requests_mock):
        """测试桥接模式容器创建"""
        # 模拟成功响应
        requests_mock.post(
            f"{self.base_url}/create/192.168.1.100/3/bridge_container",
            json={"code": 200, "msg": "桥接容器创建成功"},
        )

        bridge_config = {
            "gw": "192.168.1.1",
            "ip": "192.168.1.150",
            "subnet": "255.255.255.0",
        }

        result = self.client.create_android_container(
            ip="192.168.1.100",
            index=3,
            name="bridge_container",
            bridge_config=bridge_config,
        )

        assert result["code"] == 200

        # 验证请求体包含桥接配置
        last_request = requests_mock.last_request
        import json

        request_body = json.loads(last_request.text)
        assert request_body == bridge_config

    def test_create_android_container_invalid_bridge_config(self):
        """测试无效桥接配置"""
        # 测试非字典类型的桥接配置
        with pytest.raises(MYTSDKError, match="桥接配置必须是字典类型"):
            self.client.create_android_container(
                ip="192.168.1.100", index=1, name="test", bridge_config="invalid"
            )

        # 测试缺少必需字段的桥接配置
        with pytest.raises(MYTSDKError, match="桥接配置缺少必需字段"):
            self.client.create_android_container(
                ip="192.168.1.100",
                index=1,
                name="test",
                bridge_config={"gw": "192.168.1.1"},  # 缺少ip和subnet
            )

    @pytest.mark.skipif(not HAS_REQUESTS_MOCK, reason="requests_mock not available")
    def test_create_android_container_optional_params(self, requests_mock):
        """测试可选参数处理"""
        # 模拟成功响应
        requests_mock.post(
            f"{self.base_url}/create/192.168.1.100/4/optional_test",
            json={"code": 200, "msg": "成功"},
        )

        result = self.client.create_android_container(
            ip="192.168.1.100",
            index=4,
            name="optional_test",
            image_addr="test_image",
            mac="aa:bb:cc:dd:ee:ff",
            s5ip="127.0.0.1",
            s5port=1080,
            s5user="user",
            s5pwd="pass",
            initdev="device123",
            yktid="tid123",
            img_url="http://example.com/image.img",
        )

        assert result["code"] == 200

        # 验证可选参数被正确添加到URL
        last_request = requests_mock.last_request
        assert "image_addr=test_image" in last_request.url
        assert "mac=aa%3Abb%3Acc%3Add%3Aee%3Aff" in last_request.url  # URL编码的冒号
        assert "s5ip=127.0.0.1" in last_request.url
        assert "s5port=1080" in last_request.url
        assert "img_url=http%3A%2F%2Fexample.com%2Fimage.img" in last_request.url

    @pytest.mark.skipif(not HAS_REQUESTS_MOCK, reason="requests_mock not installed")
    def test_create_a1_android_container_basic(self, requests_mock):
        """测试创建A1安卓容器 - 基础功能"""
        # 模拟API响应
        requests_mock.post(
            f"{self.base_url}/create_A1/192.168.1.100/1/test_container",
            json={
                "code": 0,
                "message": "A1容器创建成功",
                "data": {"container_id": "a1_test123"},
            },
        )

        result = self.client.create_a1_android_container(
            ip="192.168.1.100", index=1, name="test_container"
        )

        assert result["code"] == 0
        assert "container_id" in result["data"]

    @pytest.mark.skipif(not HAS_REQUESTS_MOCK, reason="requests_mock not installed")
    def test_create_a1_android_container_advanced(self, requests_mock):
        """测试创建A1安卓容器 - 高级配置"""
        # 模拟API响应
        requests_mock.post(
            f"{self.base_url}/create_A1/192.168.1.100/2/advanced_container",
            json={
                "code": 0,
                "message": "A1容器创建成功",
                "data": {"container_id": "a1_advanced123"},
            },
        )

        result = self.client.create_a1_android_container(
            ip="192.168.1.100",
            index=2,
            name="advanced_container",
            sandbox=1,
            sandbox_size=32,
            memory=4096,
            cpu="0,1,2,3",
            resolution=1,
            width=1080,
            height=1920,
            dpi=480,
            fps=60,
            dns="8.8.8.8",
        )

        assert result["code"] == 0
        assert "container_id" in result["data"]

    @pytest.mark.skipif(not HAS_REQUESTS_MOCK, reason="requests_mock not installed")
    def test_create_p1_android_container_basic(self, requests_mock):
        """测试创建P1安卓容器 - 基础功能"""
        # 模拟API响应
        requests_mock.post(
            f"{self.base_url}/create_P1/192.168.1.100/1/test_container",
            json={
                "code": 0,
                "message": "P1容器创建成功",
                "data": {"container_id": "p1_test123"},
            },
        )

        result = self.client.create_p1_android_container(
            ip="192.168.1.100", index=1, name="test_container"
        )

        assert result["code"] == 0
        assert "container_id" in result["data"]

    @pytest.mark.skipif(not HAS_REQUESTS_MOCK, reason="requests_mock not installed")
    def test_create_p1_android_container_with_proxy(self, requests_mock):
        """测试创建P1安卓容器 - 代理配置"""
        # 模拟API响应
        requests_mock.post(
            f"{self.base_url}/create_P1/192.168.1.100/3/proxy_container",
            json={
                "code": 0,
                "message": "P1容器创建成功",
                "data": {"container_id": "p1_proxy123"},
            },
        )

        result = self.client.create_p1_android_container(
            ip="192.168.1.100",
            index=3,
            name="proxy_container",
            s5ip="192.168.1.200",
            s5port=1080,
            s5user="proxy_user",
            s5pwd="proxy_pass",
            memory=2048,
            dns="8.8.8.8",
        )

        assert result["code"] == 0
        assert "container_id" in result["data"]

    @pytest.mark.skipif(not HAS_REQUESTS_MOCK, reason="requests_mock not installed")
    def test_create_container_with_port_mapping(self, requests_mock):
        """测试创建容器 - 端口映射配置"""
        # 模拟API响应
        requests_mock.post(
            f"{self.base_url}/create_A1/192.168.1.100/5/port_mapping_container",
            json={
                "code": 0,
                "message": "容器创建成功",
                "data": {"container_id": "port_mapping123"},
            },
        )

        result = self.client.create_a1_android_container(
            ip="192.168.1.100",
            index=5,
            name="port_mapping_container",
            tcp_map_port="{20000:50001, 30000:50002}",
            udp_map_port="{25000:50003, 35000:50004}",
            adbport=55555,
            rpaport=56666,
        )

        assert result["code"] == 0
        assert "container_id" in result["data"]

    def test_get_android_detail_basic(self, requests_mock):
        """测试获取安卓实例详细信息 - 基础功能"""
        mock_response = {
            "code": 200,
            "msg": {
                "cpuset": "",
                "dns": "223.5.5.5",
                "dpi": "320",
                "fps": "24",
                "hardware": "rk30board",
                "height": "1280",
                "id": "4bf001ea0a8196a3647b47375edab55e617869857eba750aa779ff78e6074a59",
                "image": "192.168.197.16:5000/rk3588-rksdk12l:dev",
                "index": 5,
                "ip": "",
                "local_ip": "172.17.0.12",
                "memory": 0,
                "name": "f9bae6760aa65e76b6f9d5a71f002302_5_t15",
                "network": "default",
                "rpa": "7105",
                "status": "running",
                "width": "720",
            },
        }

        requests_mock.get(
            f"{self.base_url}/get_android_detail/192.168.1.100/test_container",
            json=mock_response,
        )

        result = self.client.get_android_detail(
            ip="192.168.1.100", name="test_container"
        )

        assert result["code"] == 200
        assert result["msg"]["status"] == "running"
        assert result["msg"]["dpi"] == "320"
        assert result["msg"]["width"] == "720"
        assert result["msg"]["height"] == "1280"

    def test_get_host_version_basic(self, requests_mock):
        """测试获取主机版本 - 基础功能"""
        requests_mock.get(
            f"{self.base_url}/get_host_ver/192.168.1.100",
            json={"code": 200, "msg": "v2.1.0"},
        )

        result = self.client.get_host_version(ip="192.168.1.100")

        assert result["code"] == 200
        assert "v2.1.0" in result["msg"]

    def test_upload_file_to_android_basic(self, requests_mock):
        """测试上传文件到安卓容器 - 基础功能"""
        requests_mock.get(
            f"{self.base_url}/upload_file/192.168.1.100/test_container",
            json={"code": 200, "msg": "文件上传成功"},
        )

        result = self.client.upload_file_to_android(
            ip="192.168.1.100", name="test_container", local_file="/home/user/test.apk"
        )

        assert result["code"] == 200
        assert "文件上传成功" in result["msg"]

    def test_random_device_info_basic(self, requests_mock):
        """测试随机设备信息 - 基础功能"""
        requests_mock.get(
            f"{self.base_url}/random_devinfo/192.168.1.100/test_container",
            json={"code": 200, "msg": "设备信息随机成功"},
        )

        result = self.client.random_device_info(
            ip="192.168.1.100", name="test_container"
        )

        assert result["code"] == 200
        assert "设备信息随机成功" in result["msg"]

    def test_random_device_info_with_params(self, requests_mock):
        """测试随机设备信息 - 带参数"""
        requests_mock.get(
            f"{self.base_url}/random_devinfo/192.168.1.100/test_container",
            json={"code": 200, "msg": "设备信息随机成功"},
        )

        result = self.client.random_device_info(
            ip="192.168.1.100",
            name="test_container",
            userip="192.168.1.200",
            modelid="samsung_s21",
        )

        assert result["code"] == 200
        assert "设备信息随机成功" in result["msg"]

    def test_random_device_info_async_basic(self, requests_mock):
        """测试异步随机设备信息 - 基础功能"""
        requests_mock.get(
            f"{self.base_url}/random_devinfo_async/192.168.1.100/test_container",
            json={"code": 200, "msg": "异步设备信息随机启动"},
        )

        result = self.client.random_device_info_async(
            ip="192.168.1.100", name="test_container"
        )

        assert result["code"] == 200
        assert "异步设备信息随机启动" in result["msg"]

    def test_random_device_info_async2_request(self, requests_mock):
        """测试异步随机设备信息2 - 请求模式"""
        requests_mock.get(
            f"{self.base_url}/random_devinfo_async2/192.168.1.100/test_container/request",
            json={"code": 200, "msg": "异步请求已提交"},
        )

        result = self.client.random_device_info_async2(
            ip="192.168.1.100",
            name="test_container",
            act="request",
            userip="192.168.1.150",
        )

        assert result["code"] == 200
        assert "异步请求已提交" in result["msg"]

    def test_random_device_info_async2_query(self, requests_mock):
        """测试异步随机设备信息2 - 查询模式"""
        requests_mock.get(
            f"{self.base_url}/random_devinfo_async2/192.168.1.100/test_container/query",
            json={"code": 202, "msg": "任务进行中"},
        )

        result = self.client.random_device_info_async2(
            ip="192.168.1.100", name="test_container", act="query"
        )

        assert result["code"] == 202
        assert "任务进行中" in result["msg"]

    def test_set_custom_device_info_basic(self, requests_mock):
        """测试自定义设备信息 - 基础功能"""
        requests_mock.post(
            f"{self.base_url}/set_custom_devinfo/192.168.1.100/test_container",
            json={"code": 200, "msg": "自定义设备信息设置成功"},
        )

        device_data = '{"device_model": "SM-G991B", "manufacturer": "Samsung"}'

        result = self.client.set_custom_device_info(
            ip="192.168.1.100", name="test_container", device_data=device_data
        )

        assert result["code"] == 200
        assert "自定义设备信息设置成功" in result["msg"]

    def test_set_custom_device_info_full_params(self, requests_mock):
        """测试自定义设备信息 - 完整参数"""
        requests_mock.post(
            f"{self.base_url}/set_custom_devinfo/192.168.1.100/test_container",
            json={"code": 200, "msg": "自定义设备信息设置成功"},
        )

        device_data = '{"device_model": "SM-G991B", "manufacturer": "Samsung"}'

        result = self.client.set_custom_device_info(
            ip="192.168.1.100",
            name="test_container",
            device_data=device_data,
            android_id="1234567890abcdef",
            imei="123456789012345",
            imsi="123456789012345",
            series_num="R58N123ABCD",
            btaddr="AA:BB:CC:DD:EE:FF",
            btname="Samsung Galaxy S21",
            wifi_mac="11:22:33:44:55:66",
            wifi_name="Galaxy-S21",
            oaid="12345678-1234-1234-1234-123456789012",
        )

        assert result["code"] == 200
        assert "自定义设备信息设置成功" in result["msg"]

    # 容器管理功能测试
    def test_get_android_containers_all(self):
        """测试获取所有安卓容器列表"""
        with patch.object(self.client, "_make_request") as mock_request:
            mock_request.return_value = {
                "code": 200,
                "msg": [
                    {
                        "Names": "container1",
                        "State": "running",
                        "data": "/mmc/data/data1",
                        "index": 1,
                        "ip": "192.168.1.100",
                    }
                ],
            }

            result = self.client.get_android_containers("192.168.1.100")

            assert result["code"] == 200
            mock_request.assert_called_once_with("GET", "/get/192.168.1.100", params={})

    def test_get_android_containers_with_params(self):
        """测试获取安卓容器列表（带参数）"""
        with patch.object(self.client, "_make_request") as mock_request:
            mock_request.return_value = {"code": 200, "msg": []}

            result = self.client.get_android_containers(
                "192.168.1.100", index="1", name="test_container"
            )

            assert result["code"] == 200
            mock_request.assert_called_once_with(
                "GET",
                "/get/192.168.1.100",
                params={"index": "1", "name": "test_container"},
            )

    def test_run_android_container(self):
        """测试运行安卓容器"""
        with patch.object(self.client, "_make_request") as mock_request:
            mock_request.return_value = {"code": 200, "msg": ""}

            result = self.client.run_android_container(
                "192.168.1.100", "test_container"
            )

            assert result["code"] == 200
            mock_request.assert_called_once_with(
                "GET", "/run/192.168.1.100/test_container", params={}
            )

    def test_run_android_container_force(self):
        """测试强制运行安卓容器"""
        with patch.object(self.client, "_make_request") as mock_request:
            mock_request.return_value = {"code": 200, "msg": ""}

            result = self.client.run_android_container(
                "192.168.1.100", "test_container", force="1"
            )

            assert result["code"] == 200
            mock_request.assert_called_once_with(
                "GET", "/run/192.168.1.100/test_container", params={"force": "1"}
            )

    def test_upload_url_file_to_android(self):
        """测试从URL上传文件到安卓容器"""
        with patch.object(self.client, "_make_request") as mock_request:
            mock_request.return_value = {"code": 200, "msg": ""}

            result = self.client.upload_url_file_to_android(
                "192.168.1.100",
                "test_container",
                "https://example.com/file.apk",
                "/sdcard/Download/file.apk",
                3,
            )

            assert result["code"] == 200
            mock_request.assert_called_once_with(
                "POST",
                "/upload2_file/192.168.1.100/test_container",
                data={
                    "url": "https://example.com/file.apk",
                    "remote_path": "/sdcard/Download/file.apk",
                    "retry": 3,
                },
            )

    def test_get_clipboard_content(self):
        """测试获取剪切板内容"""
        with patch.object(self.client, "_make_request") as mock_request:
            mock_request.return_value = {"code": 200, "msg": "clipboard content"}

            result = self.client.get_clipboard_content(
                "192.168.1.100", "test_container"
            )

            assert result["code"] == 200
            mock_request.assert_called_once_with(
                "GET", "/clipboard_get/192.168.1.100/test_container"
            )

    def test_set_clipboard_content(self):
        """测试设置剪切板内容"""
        with patch.object(self.client, "_make_request") as mock_request:
            mock_request.return_value = {"code": 200, "msg": ""}

            result = self.client.set_clipboard_content(
                "192.168.1.100", "test_container", "Hello World"
            )

            assert result["code"] == 200
            mock_request.assert_called_once_with(
                "GET",
                "/clipboard_set/192.168.1.100/test_container",
                params={"text": "Hello World"},
            )

    def test_download_file_from_android(self):
        """测试从安卓下载文件"""
        with patch.object(self.client, "_make_request") as mock_request:
            mock_request.return_value = {"code": 200, "msg": "/local/path/file.apk"}

            result = self.client.download_file_from_android(
                "192.168.1.100",
                "test_container",
                "/sdcard/Download/file.apk",
                "/local/path/file.apk",
            )

            assert result["code"] == 200
            mock_request.assert_called_once_with(
                "GET",
                "/down_file/192.168.1.100/test_container",
                params={
                    "path": "/sdcard/Download/file.apk",
                    "local": "/local/path/file.apk",
                },
            )

    def test_get_android_boot_status(self):
        """测试获取安卓启动状态"""
        with patch.object(self.client, "_make_request") as mock_request:
            mock_request.return_value = {"code": 200, "msg": "boot completed"}

            result = self.client.get_android_boot_status(
                "192.168.1.100", "test_container", isblock=1, timeout=60, init_devinfo=1
            )

            assert result["code"] == 200
            mock_request.assert_called_once_with(
                "GET",
                "/get_android_boot_status/192.168.1.100/test_container",
                params={"isblock": 1, "timeout": 60, "init_devinfo": 1},
            )

    def test_install_apk(self):
        """测试安装APK"""
        with patch.object(self.client, "_make_request") as mock_request:
            mock_request.return_value = {"code": 200, "msg": ""}

            result = self.client.install_apk(
                "192.168.1.100", "test_container", "/path/to/app.apk"
            )

            assert result["code"] == 200
            mock_request.assert_called_once_with(
                "GET",
                "/install_apk/192.168.1.100/test_container",
                params={"local": "/path/to/app.apk"},
            )

    def test_install_apk_from_url(self):
        """测试从URL安装APK"""
        with patch.object(self.client, "_make_request") as mock_request:
            mock_request.return_value = {"code": 200, "msg": ""}

            result = self.client.install_apk_from_url(
                "192.168.1.100", "test_container", "https://example.com/app.apk", 3
            )

            assert result["code"] == 200
            mock_request.assert_called_once_with(
                "POST",
                "/install_apk_fromurl/192.168.1.100/test_container",
                data={"url": "https://example.com/app.apk", "retry": 3},
            )

    def test_set_app_root_permission(self):
        """测试设置应用Root权限"""
        with patch.object(self.client, "_make_request") as mock_request:
            mock_request.return_value = {"code": 200, "msg": ""}

            result = self.client.set_app_root_permission(
                "192.168.1.100", "test_container", "com.example.app"
            )

            assert result["code"] == 200
            mock_request.assert_called_once_with(
                "GET", "/root_app/192.168.1.100/test_container/com.example.app"
            )

    def test_run_app(self):
        """测试运行应用"""
        with patch.object(self.client, "_make_request") as mock_request:
            mock_request.return_value = {"code": 200, "msg": ""}

            result = self.client.run_app(
                "192.168.1.100", "test_container", "com.example.app"
            )

            assert result["code"] == 200
            mock_request.assert_called_once_with(
                "GET", "/run_apk/192.168.1.100/test_container/com.example.app"
            )

    def test_take_screenshot(self):
        """测试获取截图"""
        with patch.object(self.client, "_make_request") as mock_request:
            mock_request.return_value = {
                "code": 200,
                "msg": "base64_image_data",
                "url": "http://192.168.1.100:8089/screenshot.png",
            }

            result = self.client.take_screenshot("192.168.1.100", "test_container", 3)

            assert result["code"] == 200
            mock_request.assert_called_once_with(
                "GET", "/screenshots/192.168.1.100/test_container/3"
            )

    def test_set_app_all_permissions(self):
        """测试设置应用所有权限"""
        with patch.object(self.client, "_make_request") as mock_request:
            mock_request.return_value = {"code": 200, "msg": ""}

            result = self.client.set_app_all_permissions(
                "192.168.1.100", "test_container", "com.example.app"
            )

            assert result["code"] == 200
            mock_request.assert_called_once_with(
                "GET",
                "/set_app_permissions/192.168.1.100/test_container/com.example.app",
            )

    def test_set_app_resolution_filter(self):
        """测试设置分辨率感知白名单"""
        with patch.object(self.client, "_make_request") as mock_request:
            mock_request.return_value = {"code": 200, "msg": ""}

            result = self.client.set_app_resolution_filter(
                "192.168.1.100", "test_container", "com.example.app", 1
            )

            assert result["code"] == 200
            mock_request.assert_called_once_with(
                "GET",
                "/set_app_resloution_filter/192.168.1.100/test_container/com.example.app/1",
            )

    def test_set_audio_playback(self):
        """测试音频播放控制"""
        with patch.object(self.client, "_make_request") as mock_request:
            mock_request.return_value = {"code": 200, "msg": ""}

            result = self.client.set_audio_playback(
                "192.168.1.100", "test_container", "play", "/sdcard/Music/test.mp3"
            )

            assert result["code"] == 200
            mock_request.assert_called_once_with(
                "GET",
                "/set_audio/192.168.1.100/test_container/play",
                params={"path": "/sdcard/Music/test.mp3"},
            )

    def test_execute_adb_command(self):
        """测试执行ADB命令"""
        with patch.object(self.client, "_make_request") as mock_request:
            mock_request.return_value = {"code": 200, "msg": "command output"}

            result = self.client.execute_adb_command(
                "192.168.1.100", "test_container", "pm list packages"
            )

            assert result["code"] == 200
            mock_request.assert_called_once_with(
                "POST",
                "/shell/192.168.1.100/test_container",
                data={"cmd": "pm list packages"},
            )

    def test_execute_adb_command2(self):
        """测试执行ADB命令2"""
        with patch.object(self.client, "_make_request") as mock_request:
            mock_request.return_value = {"code": 200, "msg": "command output"}

            result = self.client.execute_adb_command2(
                "192.168.1.100", "test_container", "getprop ro.build.version.release"
            )

            assert result["code"] == 200
            mock_request.assert_called_once_with(
                "POST",
                "/shell2/192.168.1.100/test_container",
                data={"cmd": "getprop ro.build.version.release"},
            )

    def test_uninstall_apk(self):
        """测试卸载APK"""
        with patch.object(self.client, "_make_request") as mock_request:
            mock_request.return_value = {"code": 200, "msg": ""}

            result = self.client.uninstall_apk(
                "192.168.1.100", "test_container", "com.example.app"
            )

            assert result["code"] == 200
            mock_request.assert_called_once_with(
                "GET", "/uninstall_apk/192.168.1.100/test_container/com.example.app"
            )

    def test_upload_google_cert(self):
        """测试上传谷歌证书"""
        with patch.object(self.client, "_make_request") as mock_request:
            mock_request.return_value = {"code": 200, "msg": ""}

            result = self.client.upload_google_cert(
                "192.168.1.100", "test_container", "/path/to/cert.p12"
            )

            assert result["code"] == 200
            mock_request.assert_called_once_with(
                "GET",
                "/upload_google_cert/192.168.1.100/test_container",
                params={"local": "/path/to/cert.p12"},
            )

    def test_set_s5_filter_url(self):
        """测试设置S5域名过滤"""
        with patch.object(self.client, "_make_request") as mock_request:
            mock_request.return_value = {"code": 200, "msg": ""}

            result = self.client.set_s5_filter_url(
                "192.168.1.100", "test_container", "['www.baidu.com','qq.com']"
            )

            assert result["code"] == 200
            mock_request.assert_called_once_with(
                "POST",
                "/s5_filter_url/192.168.1.100/test_container",
                data={"url_list": "['www.baidu.com','qq.com']"},
            )

    def test_query_s5_connection(self):
        """测试查询S5连接信息"""
        with patch.object(self.client, "_make_request") as mock_request:
            mock_request.return_value = {"code": 200, "msg": "connection info"}

            result = self.client.query_s5_connection("192.168.1.100", "test_container")

            assert result["code"] == 200
            mock_request.assert_called_once_with(
                "GET", "/s5_query/192.168.1.100/test_container"
            )


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
