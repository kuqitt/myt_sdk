# -*- coding: utf-8 -*-
"""
MYT API客户端新增方法测试
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
    """检查是否安装了requests_mock"""
    return HAS_REQUESTS_MOCK


class TestMYTAPIClientNewMethods:
    """测试MYT API客户端新增方法"""

    def setup_method(self):
        """设置测试环境"""
        self.base_url = "http://127.0.0.1:5000"
        self.client = MYTAPIClient(base_url=self.base_url)

    @pytest.mark.skipif(not HAS_REQUESTS_MOCK, reason="requests_mock not installed")
    def test_set_s5_connection_basic(self, requests_mock):
        """测试设置S5连接 - 基础功能"""
        requests_mock.get(
            f"{self.base_url}/s5_set/192.168.1.100/test_container",
            json={"code": 200, "msg": "S5连接设置成功"},
        )

        result = self.client.set_s5_connection(
            ip="192.168.1.100", name="test_container"
        )

        assert result["code"] == 200
        assert "S5连接设置成功" in result["msg"]

    @pytest.mark.skipif(not HAS_REQUESTS_MOCK, reason="requests_mock not installed")
    def test_set_s5_connection_with_params(self, requests_mock):
        """测试设置S5连接 - 带参数"""
        requests_mock.get(
            f"{self.base_url}/s5_set/192.168.1.100/test_container",
            json={"code": 200, "msg": "S5连接设置成功"},
        )

        result = self.client.set_s5_connection(
            ip="192.168.1.100",
            name="test_container",
            s5ip="127.0.0.1",
            s5port="1080",
            s5user="user",
            s5pwd="pass",
            domain_mode=2,
        )

        assert result["code"] == 200

        # 验证参数被正确添加到URL
        last_request = requests_mock.last_request
        assert "s5ip=127.0.0.1" in last_request.url
        assert "s5port=1080" in last_request.url
        assert "s5user=user" in last_request.url
        assert "s5pwd=pass" in last_request.url
        assert "domain_mode=2" in last_request.url

    @pytest.mark.skipif(not HAS_REQUESTS_MOCK, reason="requests_mock not installed")
    def test_stop_s5_connection(self, requests_mock):
        """测试关闭S5连接"""
        requests_mock.get(
            f"{self.base_url}/s5_stop/192.168.1.100/test_container",
            json={"code": 200, "msg": "S5连接已关闭"},
        )

        result = self.client.stop_s5_connection(
            ip="192.168.1.100", name="test_container"
        )

        assert result["code"] == 200
        assert "S5连接已关闭" in result["msg"]

    @pytest.mark.skipif(not HAS_REQUESTS_MOCK, reason="requests_mock not installed")
    def test_get_camera_stream(self, requests_mock):
        """测试获取摄像头推流地址和类型"""
        mock_response = {
            "code": 200,
            "msg": {
                "stream_url": "rtmp://192.168.1.100:1935/live/stream",
                "stream_type": "rtmp",
            },
        }

        requests_mock.get(
            f"{self.base_url}/get_cam_stream/192.168.1.100/test_container",
            json=mock_response,
        )

        result = self.client.get_camera_stream(
            ip="192.168.1.100", name="test_container"
        )

        assert result["code"] == 200
        assert "stream_url" in result["msg"]
        assert "stream_type" in result["msg"]

    @pytest.mark.skipif(not HAS_REQUESTS_MOCK, reason="requests_mock not installed")
    def test_set_camera_rotation(self, requests_mock):
        """测试设置摄像头旋转"""
        requests_mock.get(
            f"{self.base_url}/set_cam_rot/192.168.1.100/test_container/1/0",
            json={"code": 200, "msg": "摄像头旋转设置成功"},
        )

        result = self.client.set_camera_rotation(
            ip="192.168.1.100",
            name="test_container",
            rot=1,  # 90度旋转
            face=0,  # 不镜像
        )

        assert result["code"] == 200
        assert "摄像头旋转设置成功" in result["msg"]

    @pytest.mark.skipif(not HAS_REQUESTS_MOCK, reason="requests_mock not installed")
    def test_set_camera_stream(self, requests_mock):
        """测试设置摄像头推流地址和类型"""
        requests_mock.post(
            f"{self.base_url}/set_cam_stream/192.168.1.100/test_container/1",
            json={"code": 200, "msg": "摄像头推流设置成功"},
        )

        result = self.client.set_camera_stream(
            ip="192.168.1.100",
            name="test_container",
            v_type=1,  # rtmp视频流
            resolution=1,  # 1920x1080@30
            addr="rtmp://example.com/live/stream",
        )

        assert result["code"] == 200
        assert "摄像头推流设置成功" in result["msg"]

    @pytest.mark.skipif(not HAS_REQUESTS_MOCK, reason="requests_mock not installed")
    def test_set_motion_sensitivity(self, requests_mock):
        """测试设置运动传感器灵敏度"""
        requests_mock.get(
            f"{self.base_url}/set_motion_sensitivity/192.168.1.100/test_container/500",
            json={"code": 200, "msg": "运动传感器灵敏度设置成功"},
        )

        result = self.client.set_motion_sensitivity(
            ip="192.168.1.100", name="test_container", factor=500
        )

        assert result["code"] == 200
        assert "运动传感器灵敏度设置成功" in result["msg"]

    @pytest.mark.skipif(not HAS_REQUESTS_MOCK, reason="requests_mock not installed")
    def test_set_shake_status(self, requests_mock):
        """测试设置摇一摇状态"""
        requests_mock.get(
            f"{self.base_url}/set_shake/192.168.1.100/test_container/1",
            json={"code": 200, "msg": "摇一摇状态设置成功"},
        )

        result = self.client.set_shake_status(
            ip="192.168.1.100", name="test_container", enable=1  # 开启
        )

        assert result["code"] == 200
        assert "摇一摇状态设置成功" in result["msg"]

    @pytest.mark.skipif(not HAS_REQUESTS_MOCK, reason="requests_mock not installed")
    def test_set_ip_location(self, requests_mock):
        """测试IP智能定位"""
        requests_mock.get(
            f"{self.base_url}/set_ipLocation/192.168.1.100/test_container/zh",
            json={"code": 200, "msg": "IP智能定位设置成功"},
        )

        result = self.client.set_ip_location(
            ip="192.168.1.100", name="test_container", language="zh"  # 中文
        )

        assert result["code"] == 200
        assert "IP智能定位设置成功" in result["msg"]

    @pytest.mark.skipif(not HAS_REQUESTS_MOCK, reason="requests_mock not installed")
    def test_set_device_location(self, requests_mock):
        """测试设置设备经纬度信息"""
        requests_mock.get(
            f"{self.base_url}/set_location/192.168.1.100/test_container",
            json={"code": 200, "msg": "设备位置设置成功"},
        )

        result = self.client.set_device_location(
            ip="192.168.1.100",
            name="test_container",
            lat=39.9042,  # 北京纬度
            lng=116.4074,  # 北京经度
        )

        assert result["code"] == 200
        assert "设备位置设置成功" in result["msg"]

        # 验证参数被正确添加到URL
        last_request = requests_mock.last_request
        assert "lat=39.9042" in last_request.url
        assert "lng=116.4074" in last_request.url

    @pytest.mark.skipif(not HAS_REQUESTS_MOCK, reason="requests_mock not installed")
    def test_preprocess_video(self, requests_mock):
        """测试预处理视频文件"""
        requests_mock.get(
            f"{self.base_url}/pre_deal_video",
            json={"code": 200, "msg": "视频预处理完成"},
        )

        result = self.client.preprocess_video(path="/path/to/video.mp4")

        assert result["code"] == 200
        assert "视频预处理完成" in result["msg"]

        # 验证参数被正确添加到URL
        last_request = requests_mock.last_request
        assert "path=%2Fpath%2Fto%2Fvideo.mp4" in last_request.url
