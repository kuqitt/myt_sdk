#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MYT SDK API客户端

提供与MYT SDK服务器通信的接口封装
"""

import logging
from typing import Any, Dict, List, Optional
from urllib.parse import urljoin

import requests

from .exceptions import MYTSDKError

logger = logging.getLogger(__name__)


class MYTAPIClient:
    """MYT API客户端类"""

    def __init__(self, base_url: str = "http://127.0.0.1:5000", timeout: int = 30,):
        """
        初始化API客户端

        Args:
            base_url: API服务器基础URL，默认为127.0.0.1:5000
            timeout: 请求超时时间（秒），默认30秒
        """
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update(
            {"User-Agent": "MYT-SDK-Client/1.0.0", "Content-Type": "application/json"}
        )

        logger.info(f"MYT API客户端初始化完成，服务器地址: {self.base_url}")

    def _make_request(self, method: str, endpoint: str, **kwargs) -> Dict[str, Any]:
        """
        发送HTTP请求的通用方法

        Args:
            method: HTTP方法 (GET, POST, PUT, DELETE等)
            endpoint: API端点路径
            **kwargs: 传递给requests的其他参数

        Returns:
            API响应的JSON数据

        Raises:
            MYTSDKError: 请求失败时抛出
        """
        
        url = urljoin(self.base_url + "/", endpoint.lstrip("/"))

        try:
            logger.debug(f"发送{method}请求: {url}")
            response = self.session.request(
                method=method, url=url, timeout=self.timeout, **kwargs
            )

            # 检查HTTP状态码
            response.raise_for_status()

            # 解析JSON响应
            try:
                data = response.json()
                logger.debug(f"API响应: {data}")
                return data
            except ValueError as e:
                raise MYTSDKError(f"API响应不是有效的JSON格式: {str(e)}")

        except requests.exceptions.Timeout:
            raise MYTSDKError(f"请求超时: {url}")
        except requests.exceptions.ConnectionError:
            raise MYTSDKError(f"连接失败: {url}")
        except requests.exceptions.HTTPError as e:
            raise MYTSDKError(f"HTTP错误 {e.response.status_code}: {url}")
        except Exception as e:
            raise MYTSDKError(f"请求失败: {str(e)}")

    def login(self, username: str, password: str) -> Dict[str, Any]:
        """
        用户登录

        Args:
            username: 用户名
            password: 密码

        Returns:
            登录响应，包含token等信息
            格式: {"code": 200, "msg": "token_string"}
        """
        url = f"{self.base_url}/login/{username}/{password}"
        try:
            response = self.session.request(method="GET", url=url, timeout=self.timeout)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            raise MYTSDKError(f"登录请求失败: {str(e)}")

    def get_version(self) -> Dict[str, Any]:
        """
        获取SDK版本信息

        Returns:
            版本信息
            格式: {"code": 200, "data": "1.0.14.30.25", "message": ""}
        """
        return self._make_request("GET", "/version")

    def query_myt_devices(self) -> Dict[str, Any]:
        """
        获取当前网络在线设备列表

        Returns:
            设备列表
            格式: {
                "code": 200,
                "message": "success",
                "data": {"192.168.181.27": "device_id"}
            }
        """
        return self._make_request("GET", "/host_api/v1/query_myt")

    def get_image_list(self, image_type: str) -> Dict[str, Any]:
        """
        获取镜像列表

        Args:
            image_type: 镜像类型，可选值: p1, q1, a1, c1

        Returns:
            镜像列表
            格式: {
                "code": 200,
                "msg": [
                    {
                        "id": "46",
                        "image": "registry.cn-hangzhou.aliyuncs.com/whsyf/dobox:rk3588-dm-base-20230807-01",
                        "name": "test_0807"
                    }
                ]
            }
        """
        if image_type not in ["p1", "q1", "a1", "c1"]:
            raise MYTSDKError(
                f"无效的镜像类型: {image_type}，支持的类型: p1, q1, a1, c1"
            )

        return self._make_request(
            "GET", "/host_api/v1/get_img_list", params={"type": image_type}
        )

    def get_device_info(self) -> Dict[str, Any]:
        """
        获取机型信息列表

        Returns:
            机型信息
            格式: {
                "code": 200,
                "msg": {
                    "HONOR": {
                        "AKA-AL10": 39
                    }
                }
            }
        """
        return self._make_request("GET", "/get_devinfo")

    def create_android_container(
        self,
        ip: str,
        index: int,
        name: str,
        sandbox: int = 0,
        sandbox_size: int = 16,
        image_addr: Optional[str] = None,
        memory: int = 0,
        cpu: Optional[str] = None,
        resolution: int = 0,
        dns: str = "223.5.5.5",
        width: int = 720,
        height: int = 1280,
        dpi: int = 320,
        fps: int = 24,
        data_res: Optional[str] = None,
        mac: Optional[str] = None,
        random_dev: int = 1,
        s5ip: Optional[str] = None,
        s5port: int = 0,
        s5user: Optional[str] = None,
        s5pwd: Optional[str] = None,
        dnstcp_mode: int = 0,
        rpaport: int = 0,
        initdev: Optional[str] = None,
        enforce: int = 1,
        yktid: Optional[str] = None,
        ykuser: Optional[str] = None,
        yktoken: Optional[str] = None,
        ykbitrate: Optional[str] = None,
        phyinput: int = 0,
        adbport: int = 0,
        timeoffset: int = 0,
        enablemeid: int = 0,
        tcp_map_port: Optional[str] = None,
        udp_map_port: Optional[str] = None,
        img_url: Optional[str] = None,
        bridge_config: Optional[Dict[str, str]] = None,
    ) -> Dict[str, Any]:
        """
        创建安卓容器

        Args:
            ip: 主机IP地址
            index: 容器索引
            name: 容器名称
            sandbox: 是否使用沙盒模式，0不使用，1使用，默认0
            sandbox_size: 沙盒空间大小，默认16
            image_addr: 镜像地址，可选参数
            memory: 内存限制大小，单位MB，默认0
            cpu: 绑定的CPU，例如"0,4"，可选
            resolution: 分辨率参数，0表示720P，1表示1080P，2表示自定义，默认0
            dns: 域名地址，默认223.5.5.5
            width: 宽度，默认720
            height: 高度，默认1280
            dpi: 分辨率，默认320
            fps: 刷新率，默认24
            data_res: 容器的资源目录，可选
            mac: 主机的MAC地址，格式如"11:11:11:11:11:11"，可选
            random_dev: 创建时是否自动随机设备信息，默认1
            s5ip: 服务器地址，可选
            s5port: 端口信息，默认0
            s5user: 用户名，可选
            s5pwd: 账户密码，可选
            dnstcp_mode: 使用dnstcp模式，默认0
            rpaport: 指定主机的RPA端口映射，默认0
            initdev: 初始时的设备信息ID，可选
            enforce: 设置严格模式，默认1
            yktid: TID，可选
            ykuser: connect_check_user，可选
            yktoken: connect_check_token，可选
            ykbitrate: bitrate，可选
            phyinput: 是否使用物理触屏输入，默认0
            adbport: ADB端口，默认0
            timeoffset: 设置已开机的时间，默认0
            enablemeid: 是否启用MEID，默认0
            tcp_map_port: TCP端口映射，格式"{20000:20001, 30000:30001}"，可选
            udp_map_port: UDP端口映射，格式"{20000:20001, 30000:30001}"，可选
            img_url: URL镜像地址，可选
            bridge_config: 桥接模式配置，包含gw、ip、subnet字段，可选

        Returns:
            创建结果

        Raises:
            MYTSDKError: 参数验证失败或请求失败时抛出
        """
        # 构建端点URL
        endpoint = f"/dc_api/v1/create/{ip}/{index}/{name}"

        # 构建查询参数
        params = {
            "sandbox": sandbox,
            "sandbox_size": sandbox_size,
            "memory": memory,
            "resolution": resolution,
            "dns": dns,
            "width": width,
            "height": height,
            "dpi": dpi,
            "fps": fps,
            "random_dev": random_dev,
            "s5port": s5port,
            "dnstcp_mode": dnstcp_mode,
            "rpaport": rpaport,
            "enforce": enforce,
            "phyinput": phyinput,
            "adbport": adbport,
            "timeoffset": timeoffset,
            "enablemeid": enablemeid,
        }

        # 添加可选的字符串参数
        optional_str_params = {
            "image_addr": image_addr,
            "cpu": cpu,
            "data_res": data_res,
            "mac": mac,
            "s5ip": s5ip,
            "s5user": s5user,
            "s5pwd": s5pwd,
            "initdev": initdev,
            "yktid": yktid,
            "ykuser": ykuser,
            "yktoken": yktoken,
            "ykbitrate": ykbitrate,
            "tcp_map_port": tcp_map_port,
            "udp_map_port": udp_map_port,
            "img_url": img_url,
        }

        # 只添加非空的可选参数
        for key, value in optional_str_params.items():
            if value is not None:
                params[key] = value

        # 准备请求参数
        request_kwargs = {"params": params}

        # 如果提供了桥接配置，添加到请求体
        if bridge_config:
            if not isinstance(bridge_config, dict):
                raise MYTSDKError("桥接配置必须是字典类型")

            required_fields = ["gw", "ip", "subnet"]
            for field in required_fields:
                if field not in bridge_config:
                    raise MYTSDKError(f"桥接配置缺少必需字段: {field}")

            request_kwargs["json"] = bridge_config

        return self._make_request("POST", endpoint, **request_kwargs)

    def create_a1_android_container(
        self,
        ip,
        index,
        name,
        sandbox=0,
        sandbox_size=16,
        image_addr=None,
        memory=0,
        cpu=None,
        resolution=0,
        dns="223.5.5.5",
        width=720,
        height=1280,
        dpi=320,
        fps=24,
        data_res=None,
        mac=None,
        random_dev=1,
        s5ip=None,
        s5port=0,
        s5user=None,
        s5pwd=None,
        dnstcp_mode=0,
        rpaport=0,
        initdev=None,
        enforce=1,
        yktid=None,
        ykuser=None,
        yktoken=None,
        ykbitrate=None,
        phyinput=0,
        adbport=0,
        timeoffset=0,
        enablemeid=0,
        tcp_map_port=None,
        udp_map_port=None,
        img_url=None,
    ):
        """
        创建A1安卓容器

        Args:
            ip (str): IP地址
            index (int): 索引
            name (str): 容器名称
            sandbox (int): 是否使用沙盒模式 0 不使用 1 使用
            sandbox_size (int): 沙盒空间大小
            image_addr (str): 镜像地址
            memory (int): 内存限制大小 单位:MB
            cpu (str): 绑定的cpu 例如: 0,4
            resolution (int): 分辨率参数 0表示720P 1表示1080P 2表示自定义
            dns (str): 域名地址
            width (int): 宽度
            height (int): 高度
            dpi (int): 分辨率
            fps (int): 刷新率
            data_res (str): 容器的资源目录
            mac (str): 主机的mac地址
            random_dev (int): 创建时是否自动随机设备信息
            s5ip (str): 服务器地址
            s5port (int): 端口信息
            s5user (str): 用户名
            s5pwd (str): 账户密码
            dnstcp_mode (int): 使用dnstcp模式
            rpaport (int): 指定主机的rpa端口映射
            initdev (str): 初始时的设备信息ID
            enforce (int): 设置严格模式
            yktid (str): TID
            ykuser (str): connect_check_user
            yktoken (str): connect_check_token
            ykbitrate (str): bitrate
            phyinput (int): 是否使用物理触屏输入
            adbport (int): adb端口
            timeoffset (int): 设置已开机的时间
            enablemeid (int): 是否启用meid
            tcp_map_port (str): tcp端口映射
            udp_map_port (str): udp端口映射
            img_url (str): url镜像地址

        Returns:
            dict: API响应结果
        """
        endpoint = f"/dc_api/v1/create_A1/{ip}/{index}/{name}"

        # 构建查询参数
        params = {
            "sandbox": sandbox,
            "sandbox_size": sandbox_size,
            "memory": memory,
            "resolution": resolution,
            "dns": dns,
            "width": width,
            "height": height,
            "dpi": dpi,
            "fps": fps,
            "random_dev": random_dev,
            "s5port": s5port,
            "dnstcp_mode": dnstcp_mode,
            "rpaport": rpaport,
            "enforce": enforce,
            "phyinput": phyinput,
            "adbport": adbport,
            "timeoffset": timeoffset,
            "enablemeid": enablemeid,
        }

        # 可选字符串参数
        optional_str_params = {
            "image_addr": image_addr,
            "cpu": cpu,
            "data_res": data_res,
            "mac": mac,
            "s5ip": s5ip,
            "s5user": s5user,
            "s5pwd": s5pwd,
            "initdev": initdev,
            "yktid": yktid,
            "ykuser": ykuser,
            "yktoken": yktoken,
            "ykbitrate": ykbitrate,
            "tcp_map_port": tcp_map_port,
            "udp_map_port": udp_map_port,
            "img_url": img_url,
        }

        # 只添加非空的可选参数
        for key, value in optional_str_params.items():
            if value is not None:
                params[key] = value

        return self._make_request("POST", endpoint, params=params)

    def create_p1_android_container(
        self,
        ip,
        index,
        name,
        sandbox=0,
        sandbox_size=16,
        image_addr=None,
        memory=0,
        cpu=None,
        resolution=0,
        dns="223.5.5.5",
        width=720,
        height=1280,
        dpi=320,
        fps=24,
        data_res=None,
        mac=None,
        random_dev=1,
        s5ip=None,
        s5port=0,
        s5user=None,
        s5pwd=None,
        dnstcp_mode=0,
        rpaport=0,
        initdev=None,
        enforce=1,
        yktid=None,
        ykuser=None,
        yktoken=None,
        ykbitrate=None,
        phyinput=0,
        adbport=0,
        timeoffset=0,
        enablemeid=0,
        tcp_map_port=None,
        udp_map_port=None,
        img_url=None,
    ):
        """
        创建P1安卓容器

        Args:
            ip (str): IP地址
            index (int): 索引
            name (str): 容器名称
            sandbox (int): 是否使用沙盒模式 0 不使用 1 使用
            sandbox_size (int): 沙盒空间大小
            image_addr (str): 镜像地址
            memory (int): 内存限制大小 单位:MB
            cpu (str): 绑定的cpu 例如: 0,4
            resolution (int): 分辨率参数 0表示720P 1表示1080P 2表示自定义
            dns (str): 域名地址
            width (int): 宽度
            height (int): 高度
            dpi (int): 分辨率
            fps (int): 刷新率
            data_res (str): 容器的资源目录
            mac (str): 主机的mac地址
            random_dev (int): 创建时是否自动随机设备信息
            s5ip (str): 服务器地址
            s5port (int): 端口信息
            s5user (str): 用户名
            s5pwd (str): 账户密码
            dnstcp_mode (int): 使用dnstcp模式
            rpaport (int): 指定主机的rpa端口映射
            initdev (str): 初始时的设备信息ID
            enforce (int): 设置严格模式
            yktid (str): TID
            ykuser (str): connect_check_user
            yktoken (str): connect_check_token
            ykbitrate (str): bitrate
            phyinput (int): 是否使用物理触屏输入
            adbport (int): adb端口
            timeoffset (int): 设置已开机的时间
            enablemeid (int): 是否启用meid
            tcp_map_port (str): tcp端口映射
            udp_map_port (str): udp端口映射
            img_url (str): url镜像地址

        Returns:
            dict: API响应结果
        """
        endpoint = f"/dc_api/v1/create_P1/{ip}/{index}/{name}"

        # 构建查询参数
        params = {
            "sandbox": sandbox,
            "sandbox_size": sandbox_size,
            "memory": memory,
            "resolution": resolution,
            "dns": dns,
            "width": width,
            "height": height,
            "dpi": dpi,
            "fps": fps,
            "random_dev": random_dev,
            "s5port": s5port,
            "dnstcp_mode": dnstcp_mode,
            "rpaport": rpaport,
            "enforce": enforce,
            "phyinput": phyinput,
            "adbport": adbport,
            "timeoffset": timeoffset,
            "enablemeid": enablemeid,
        }

        # 可选字符串参数
        optional_str_params = {
            "image_addr": image_addr,
            "cpu": cpu,
            "data_res": data_res,
            "mac": mac,
            "s5ip": s5ip,
            "s5user": s5user,
            "s5pwd": s5pwd,
            "initdev": initdev,
            "yktid": yktid,
            "ykuser": ykuser,
            "yktoken": yktoken,
            "ykbitrate": ykbitrate,
            "tcp_map_port": tcp_map_port,
            "udp_map_port": udp_map_port,
            "img_url": img_url,
        }

        # 只添加非空的可选参数
        for key, value in optional_str_params.items():
            if value is not None:
                params[key] = value

        return self._make_request("POST", endpoint, params=params)
    # 导入容器
    def  import_container(self, ip: str, name: str, image_addr: str, imgcompress: int = 0) -> Dict[str, Any]:
        """
        导入容器

        Args:
            ip (str): 主机IP地址
            name (str): 容器名称
            image_addr (str): 镜像地址

        Returns:
            dict: 导入结果
        """
        """
            参数名称	是否必选	请求方式	数据类型	字段说明
            ip	必选	PATH	str	3588主机ip地址
            names	必选	query	str	容器名称，多个容器用逗号分隔
            local	必选	query	str	资源镜像的名称 默认存在当前目录 backup 下,多个路径用逗号分隔,需要与names一一对应
            imgcompress	可选	query	int	启用img文件压缩 默认为0 不启用 1 为启用
        """
        params = {
            "names": name,
            "local": image_addr,
            "imgcompress": imgcompress,
        }
        endpoint = f"/dc_api/v1/batch_export/{ip}"
        return self._make_request("GET", endpoint, params=params)

    def get_android_detail(self, ip: str, name: str) -> Dict[str, Any]:
        """
        获取安卓实例详细信息

        Args:
            ip (str): 主机IP地址
            name (str): 安卓容器名称

        Returns:
            dict: 安卓实例详细信息，包含CPU、内存、分辨率等配置
        """
        endpoint = f"/dc_api/v1/get_android_detail/{ip}/{name}"
        return self._make_request("GET", endpoint)

    def get_host_version(self, ip: str) -> Dict[str, Any]:
        """
        获取主机版本信息

        Args:
            ip (str): 主机IP地址

        Returns:
            dict: 主机版本信息
        """
        endpoint = f"/dc_api/v1/get_host_ver/{ip}"
        return self._make_request("GET", endpoint)

    def upload_file_to_android(
        self, ip: str, name: str, local_file: str
    ) -> Dict[str, Any]:
        """
        上传文件到安卓容器

        Args:
            ip (str): 主机IP地址
            name (str): 安卓容器名称
            local_file (str): 本地文件路径（必须与SDK在同一台主机上）

        Returns:
            dict: 上传结果
        """
        endpoint = f"/dc_api/v1/upload_file/{ip}/{name}"
        params = {"local": local_file}
        return self._make_request("GET", endpoint, params=params)

    def random_device_info(
        self,
        ip: str,
        name: str,
        userip: Optional[str] = None,
        modelid: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        安卓设备随机更换设备信息（同步）

        Args:
            ip (str): 主机IP地址
            name (str): 安卓容器名称
            userip (str, optional): 指定IP信息随机
            modelid (str, optional): 指定设备型号ID

        Returns:
            dict: 操作结果
        """
        endpoint = f"/and_api/v1/random_devinfo/{ip}/{name}"
        params = {}
        if userip is not None:
            params["userip"] = userip
        if modelid is not None:
            params["modelid"] = modelid

        return self._make_request("GET", endpoint, params=params if params else None)

    def random_device_info_async(
        self,
        ip: str,
        name: str,
        userip: Optional[str] = None,
        modelid: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        安卓设备随机更换设备信息（异步）

        Args:
            ip (str): 主机IP地址
            name (str): 安卓容器名称
            userip (str, optional): 指定IP信息随机
            modelid (str, optional): 指定设备型号ID

        Returns:
            dict: 异步操作结果
        """
        endpoint = f"/and_api/v1/random_devinfo_async/{ip}/{name}"
        params = {}
        if userip is not None:
            params["userip"] = userip
        if modelid is not None:
            params["modelid"] = modelid

        return self._make_request("GET", endpoint, params=params if params else None)

    def random_device_info_async2(
        self,
        ip: str,
        name: str,
        act: str,
        userip: Optional[str] = None,
        modelid: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        安卓设备随机更换设备信息（异步2）

        Args:
            ip (str): 主机IP地址
            name (str): 安卓容器名称
            act (str): 操作类型 - 'request'请求结果, 'query'获取结果, 'get'获取并清空任务进度
            userip (str, optional): 指定IP信息随机
            modelid (str, optional): 指定设备型号ID

        Returns:
            dict: 异步操作结果
        """
        endpoint = f"/and_api/v1/random_devinfo_async2/{ip}/{name}/{act}"
        params = {}
        if userip is not None:
            params["userip"] = userip
        if modelid is not None:
            params["modelid"] = modelid

        return self._make_request("GET", endpoint, params=params if params else None)

    def set_custom_device_info(
        self,
        ip: str,
        name: str,
        device_data: str,
        android_id: Optional[str] = None,
        iccid: Optional[str] = None,
        imei: Optional[str] = None,
        imsi: Optional[str] = None,
        series_num: Optional[str] = None,
        btaddr: Optional[str] = None,
        btname: Optional[str] = None,
        wifi_mac: Optional[str] = None,
        wifi_name: Optional[str] = None,
        oaid: Optional[str] = None,
        aaid: Optional[str] = None,
        vaid: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        自定义设备机型信息（数字孪生）

        注意：该接口请慎重使用，如果传入的数据异常，可能会导致系统无法开机

        Args:
            ip (str): 主机IP地址
            name (str): 安卓容器名称
            device_data (str): 导出的真机信息数据（完整设备字符串）
            android_id (str, optional): Android ID
            iccid (str, optional): ICCID
            imei (str, optional): IMEI
            imsi (str, optional): IMSI
            series_num (str, optional): 序列号
            btaddr (str, optional): 蓝牙地址
            btname (str, optional): 蓝牙名称
            wifi_mac (str, optional): WiFi MAC地址
            wifi_name (str, optional): WiFi名称
            oaid (str, optional): OAID
            aaid (str, optional): AAID
            vaid (str, optional): VAID

        Returns:
            dict: 设置结果
        """
        endpoint = f"/and_api/v1/set_custom_devinfo/{ip}/{name}"

        # 构建查询参数
        params = {}
        optional_params = {
            "androidId": android_id,
            "iccid": iccid,
            "imei": imei,
            "imsi": imsi,
            "seriesNum": series_num,
            "btaddr": btaddr,
            "btname": btname,
            "wifiMac": wifi_mac,
            "wifiName": wifi_name,
            "oaid": oaid,
            "aaid": aaid,
            "vaid": vaid,
        }

        # 只添加非空的可选参数
        for key, value in optional_params.items():
            if value is not None:
                params[key] = value

        # 设置请求体为设备数据
        request_kwargs = {
            "data": device_data,
            "headers": {"Content-Type": "text/plain"},
        }

        if params:
            request_kwargs["params"] = params

        return self._make_request("POST", endpoint, **request_kwargs)

    def get_android_containers(self, ip, index=None, name=None):
        """
        获取安卓容器列表

        Args:
            ip (str): 3588主机IP地址
            index (str, optional): 实例索引(坑位)，1-12数字
            name (str, optional): 查询指定容器的信息

        Returns:
            dict: 容器列表信息
        """
        endpoint = f"/dc_api/v1/get/{ip}"
        params = {}

        if index is not None:
            params["index"] = index
        if name is not None:
            params["name"] = name

        return self._make_request("GET", endpoint, params=params)

    def run_android_container(self, ip, name, force=None):
        """
        运行安卓容器

        Args:
            ip (str): 3588主机IP地址
            name (str): 容器名称
            force (str, optional): 是否强制运行，1为强制，0为默认

        Returns:
            dict: 运行结果
        """
        endpoint = f"/dc_api/v1/run/{ip}/{name}"
        params = {}

        if force is not None:
            params["force"] = force

        return self._make_request("GET", endpoint, params=params)

    def upload_url_file_to_android(self, ip, name, url, remote_path, retry=0):
        """
        从URL上传文件到安卓容器

        Args:
            ip (str): 3588主机IP地址
            name (str): 容器名称
            url (str): 文件的URL下载地址
            remote_path (str): Android中文件的保存绝对路径
            retry (int): 重试次数，0表示不重试

        Returns:
            dict: 上传结果
        """
        endpoint = f"/upload2_file/{ip}/{name}"
        data = {"url": url, "remote_path": remote_path, "retry": retry}

        return self._make_request("POST", endpoint, data=data)

    def get_clipboard_content(self, ip, name):
        """
        获取安卓剪切板内容

        Args:
            ip (str): 3588主机IP地址
            name (str): 容器名称

        Returns:
            dict: 剪切板内容
        """
        endpoint = f"/and_api/v1/clipboard_get/{ip}/{name}"
        return self._make_request("GET", endpoint)

    def set_clipboard_content(self, ip, name, text):
        """
        设置安卓剪切板内容

        Args:
            ip (str): 3588主机IP地址
            name (str): 容器名称
            text (str): 剪切板的内容

        Returns:
            dict: 设置结果
        """
        endpoint = f"/and_api/v1/clipboard_set/{ip}/{name}"
        params = {"text": text}

        return self._make_request("GET", endpoint, params=params)

    def download_file_from_android(self, ip, name, path, local):
        """
        从安卓实例下载文件

        Args:
            ip (str): 3588主机IP地址
            name (str): 容器名称
            path (str): 指定路径的文件
            local (str): 下载文件的本地保存路径

        Returns:
            dict: 下载结果
        """
        endpoint = f"/and_api/v1/down_file/{ip}/{name}"
        params = {"path": path, "local": local}

        return self._make_request("GET", endpoint, params=params)

   
    def get_android_boot_status(self, ip, name, isblock=0, timeout=120, init_devinfo=0):
        """
        获取安卓启动状态

        Args:
            ip (str): 3588主机IP地址
            name (str): 容器名称
            isblock (int): 是否阻塞等待，0否1是
            timeout (int): 超时时间，单位秒，默认120秒
            init_devinfo (int): 是否判断初始化设备信息完成，0不初始化1初始化

        Returns:
            dict: 启动状态
        """
        endpoint = f"/and_api/v1/get_android_boot_status/{ip}/{name}"
        params = {"isblock": isblock, "timeout": timeout, "init_devinfo": init_devinfo}

        return self._make_request("GET", endpoint, params=params)

    def install_apk(self, ip, name, local):
        """
        安装APK到安卓容器

        Args:
            ip (str): 3588主机IP地址
            name (str): 容器名称
            local (str): 本地APK文件的绝对路径

        Returns:
            dict: 安装结果
        """
        endpoint = f"/and_api/v1/install_apk/{ip}/{name}"
        params = {"local": local}

        return self._make_request("GET", endpoint, params=params)

    def install_apk_from_url(self, ip, name, url, retry=0):
        """
        从URL安装APK到安卓容器

        Args:
            ip (str): 3588主机IP地址
            name (str): 容器名称
            url (str): APK文件的URL下载地址
            retry (int): 重试次数，0表示不重试

        Returns:
            dict: 安装结果
        """
        endpoint = f"/and_api/v1/install_apk_fromurl/{ip}/{name}"
        data = {"url": url, "retry": retry}

        return self._make_request("POST", endpoint, data=data)

    def set_app_root_permission(self, ip, name, package):
        """
        设置应用Root权限

        Args:
            ip (str): 3588主机IP地址
            name (str): 容器实例名称
            package (str): 应用包名

        Returns:
            dict: 设置结果
        """
        endpoint = f"/and_api/v1/root_app/{ip}/{name}/{package}"
        return self._make_request("GET", endpoint)

    def run_app(self, ip, name, pkg):
        """
        运行应用

        Args:
            ip (str): 3588主机IP地址
            name (str): 容器实例名称
            pkg (str): 应用包名

        Returns:
            dict: 运行结果
        """
        endpoint = f"/and_api/v1/run_apk/{ip}/{name}/{pkg}"
        return self._make_request("GET", endpoint)

    def take_screenshot(self, ip, name, level):
        """
        获取设备截图

        Args:
            ip (str): 3588主机IP地址
            name (str): 容器实例名称
            level (int): 返回的截图质量，1低2中等3高清

        Returns:
            dict: 截图结果，包含URL和base64数据
        """
        endpoint = f"/and_api/v1/screenshots/{ip}/{name}/{level}"
        return self._make_request("GET", endpoint)

    def set_app_all_permissions(self, ip, name, pkg):
        """
        设置应用所有权限

        Args:
            ip (str): 3588主机IP地址
            name (str): 容器名称
            pkg (str): 应用包名

        Returns:
            dict: 设置结果
        """
        endpoint = f"/and_api/v1/set_app_permissions/{ip}/{name}/{pkg}"
        return self._make_request("GET", endpoint)

    def set_app_resolution_filter(self, ip, name, pkg, enable):
        """
        设置分辨率感知白名单

        Args:
            ip (str): 3588主机IP地址
            name (str): 容器名称
            pkg (str): 应用包名
            enable (int): 是否加入白名单，1加入0移除

        Returns:
            dict: 设置结果
        """
        endpoint = f"/and_api/v1/set_app_resloution_filter/{ip}/{name}/{pkg}/{enable}"
        return self._make_request("GET", endpoint)

    def set_audio_playback(self, ip, name, act, path=None):
        """
        播放音频设置

        Args:
            ip (str): 3588主机IP地址
            name (str): 容器名称
            act (str): 操作类型，play播放或stop停止
            path (str, optional): 云手机内部的声音文件路径

        Returns:
            dict: 操作结果
        """
        endpoint = f"/and_api/v1/set_audio/{ip}/{name}/{act}"
        params = {}

        if path is not None:
            params["path"] = path

        return self._make_request("GET", endpoint, params=params)

    def execute_adb_command(self, ip, name, cmd):
        """
        执行ADB命令

        Args:
            ip (str): 3588主机IP地址
            name (str): 容器名称
            cmd (str): 要执行的ADB命令

        Returns:
            dict: 命令执行结果
        """
        endpoint = f"/and_api/v1/shell/{ip}/{name}"
        data = {"cmd": cmd}

        return self._make_request("POST", endpoint, data=data)

    def execute_adb_command2(self, ip, name, cmd):
        """
        执行ADB命令2

        Args:
            ip (str): 3588主机IP地址
            name (str): 容器名称
            cmd (str): 要执行的ADB命令

        Returns:
            dict: 命令执行结果
        """
        endpoint = f"/and_api/v1/shell2/{ip}/{name}"
        data = {"cmd": cmd}

        return self._make_request("POST", endpoint, data=data)

    def uninstall_apk(self, ip, name, pkg):
        """
        卸载APK

        Args:
            ip (str): 3588主机IP地址
            name (str): 容器实例名称
            pkg (str): 应用包名

        Returns:
            dict: 卸载结果
        """
        endpoint = f"/and_api/v1/uninstall_apk/{ip}/{name}/{pkg}"
        return self._make_request("GET", endpoint)

    def upload_google_cert(self, ip, name, local):
        """
        上传谷歌证书

        Args:
            ip (str): 3588主机IP地址
            name (str): 容器名称
            local (str): 本地证书文件的绝对路径

        Returns:
            dict: 上传结果
        """
        endpoint = f"/and_api/v1/upload_google_cert/{ip}/{name}"
        params = {"local": local}

        return self._make_request("GET", endpoint, params=params)

    def set_s5_filter_url(self, ip, name, url_list):
        """
        设置S5域名过滤

        Args:
            ip (str): 3588主机IP地址
            name (str): 容器名称
            url_list (str): 需要过滤的域名列表，JSON格式字符串

        Returns:
            dict: 设置结果
        """
        endpoint = f"/and_api/v1/s5_filter_url/{ip}/{name}"
        data = {"url_list": url_list}

        return self._make_request("POST", endpoint, data=data)

    def query_s5_connection(self, ip, name):
        """
        查询S5连接信息

        Args:
            ip (str): 3588主机IP地址
            name (str): 容器名称

        Returns:
            dict: S5连接信息
        """
        endpoint = f"/and_api/v1/s5_query/{ip}/{name}"
        return self._make_request("GET", endpoint)

    def close(self):
        """
        关闭客户端连接
        """
        if self.session:
            self.session.close()
            logger.info("MYT API客户端连接已关闭")

    def __enter__(self):
        """上下文管理器入口"""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """上下文管理器出口"""
        self.close()

    # 便捷函数
    def set_s5_connection(
        self,
        ip: str,
        name: str,
        s5ip: Optional[str] = None,
        s5port: Optional[str] = None,
        s5user: Optional[str] = None,
        s5pwd: Optional[str] = None,
        domain_mode: Optional[int] = 1,
    ) -> Dict[str, Any]:
        """
        设置S5连接

        Args:
            ip: 3588主机IP地址
            name: 容器名称
            s5ip: S5服务器地址，可选
            s5port: S5端口地址，可选
            s5user: S5用户名，可选
            s5pwd: S5密码，可选
            domain_mode: 域名解析模式，1本地域名解析，2服务端域名解析（默认），可选

        Returns:
            dict: 设置结果
        """
        endpoint = f"/and_api/v1/s5_set/{ip}/{name}"
        params = {}

        if s5ip is not None:
            params["s5ip"] = s5ip
        if s5port is not None:
            params["s5port"] = s5port
        if s5user is not None:
            params["s5user"] = s5user
        if s5pwd is not None:
            params["s5pwd"] = s5pwd
        if domain_mode is not None:
            params["domain_mode"] = domain_mode

        return self._make_request("GET", endpoint, params=params)

    def stop_s5_connection(self, ip: str, name: str) -> Dict[str, Any]:
        """
        关闭S5连接

        Args:
            ip: 3588主机IP地址
            name: 容器名称

        Returns:
            dict: 关闭结果
        """
        endpoint = f"/and_api/v1/s5_stop/{ip}/{name}"
        return self._make_request("GET", endpoint)
    def reboot(self, ip: str, name: str) -> Dict[str, Any]:
        """
        重启容器

        Args:
            ip: 3588主机IP地址
            name: 容器名称

        Returns:
            dict: 重启结果
        """
        endpoint = f"/dc_api/v1/reboot/{ip}/{name}"
        return self._make_request("GET", endpoint)
    def get_camera_stream(self, ip: str, name: str) -> Dict[str, Any]:
        """
        获取摄像头推流地址和类型

        Args:
            ip: 3588主机IP地址
            name: 容器名称

        Returns:
            dict: 摄像头推流信息
        """
        endpoint = f"/and_api/v1/get_cam_stream/{ip}/{name}"
        return self._make_request("GET", endpoint)

    def set_camera_rotation(
        self, ip: str, name: str, rot: int, face: int
    ) -> Dict[str, Any]:
        """
        设置摄像头旋转

        Args:
            ip: 3588主机IP地址
            name: 容器名称
            rot: 旋转方向，0不旋转，1为90度，2为180度，3为270度
            face: 镜像方向，0不镜像，1镜像

        Returns:
            dict: 设置结果
        """
        endpoint = f"/and_api/v1/set_cam_rot/{ip}/{name}/{rot}/{face}"
        return self._make_request("GET", endpoint)

    def set_camera_stream(
        self,
        ip: str,
        name: str,
        v_type: int,
        resolution: Optional[int] = None,
        addr: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        设置摄像头推流地址和类型

        Args:
            ip: 主机IP地址
            name: 实例名称
            v_type: 视频类型，1为rtmp视频流或本地视频文件，2为webrtc视频流，3为本地图片或网络图片
            resolution: 摄像头分辨率，1为1920x1080@30，2为1280x720@30，可选
            addr: 资源地址，可选

        Returns:
            dict: 设置结果
        """
        endpoint = f"/and_api/v1/set_cam_stream/{ip}/{name}/{v_type}"
        params = {}
        data = {}

        if resolution is not None:
            params["resolution"] = resolution
        if addr is not None:
            data["addr"] = addr

        return self._make_request("POST", endpoint, params=params, data=data)

    def set_motion_sensitivity(self, ip: str, name: str, factor: int) -> Dict[str, Any]:
        """
        设置运动传感器灵敏度

        Args:
            ip: 3588主机IP地址
            name: 容器名称
            factor: 灵敏度，范围[0,1000]，0表示关闭，10静止，1000运动状态，开机默认值为10

        Returns:
            dict: 设置结果
        """
        endpoint = f"/and_api/v1/set_motion_sensitivity/{ip}/{name}/{factor}"
        return self._make_request("GET", endpoint)

    def set_shake_status(self, ip: str, name: str, enable: int) -> Dict[str, Any]:
        """
        设置摇一摇状态

        Args:
            ip: 3588主机IP地址
            name: 容器名称
            enable: 0关闭，1开启，默认为关闭状态

        Returns:
            dict: 设置结果
        """
        endpoint = f"/and_api/v1/set_shake/{ip}/{name}/{enable}"
        return self._make_request("GET", endpoint)

    def set_ip_location(self, ip: str, name: str, language: str) -> Dict[str, Any]:
        """
        IP智能定位 - 根据当前IP设置环境信息(GPS基站等信息)

        Args:
            ip: 3588主机IP地址
            name: 容器名称
            language: 语言代码，zh中文/en英语/fr法语/th泰国/vi越南/ja日本/ko韩国/lo老挝/in印尼

        Returns:
            dict: 设置结果
        """
        endpoint = f"/and_api/v1/set_ipLocation/{ip}/{name}/{language}"
        return self._make_request("GET", endpoint)

    def set_device_location(
        self, ip: str, name: str, lat: float, lng: float
    ) -> Dict[str, Any]:
        """
        设置设备经纬度信息

        Args:
            ip: 3588主机IP地址
            name: 容器名称
            lat: 纬度
            lng: 经度

        Returns:
            dict: 设置结果
        """
        endpoint = f"/and_api/v1/set_location/{ip}/{name}"
        params = {"lat": lat, "lng": lng}
        return self._make_request("GET", endpoint, params=params)

    def preprocess_video(self, path: str) -> Dict[str, Any]:
        """
        预处理视频文件 - 云机实例中播放视频文件卡顿时可先预处理视频文件再上传至云机中播放

        Args:
            path: 视频文件完整路径

        Returns:
            dict: 预处理结果
        """
        endpoint = "/host_api/v1/pre_deal_video"
        params = {"path": path}
        return self._make_request("GET", endpoint, params=params)

    def get_api_info(self, ip: str, name: str) -> Dict[str, Any]:
        """
        获取API的详细信息

        Args:
            ip: IP地址
            name: API名称

        Returns:
            API详细信息
            格式: {"code": 200, "msg": ""}
        """
        endpoint = f"/and_api/v1/get_api_info/{ip}/{name}"
        return self._make_request("GET", endpoint)
    def stop_android(self, ip: str, name: str) -> Dict[str, Any]:
        """
        停止安卓容器

        Args:
            ip: IP地址
            name: 实例名称

        Returns:
            API详细信息
            格式: {"code": 200, "msg": ""}
        """
        endpoint = f"/dc_api/v1/stop/{ip}/{name}"
        return self._make_request("GET", endpoint)
    def reset_android(self, ip: str, name: str) -> Dict[str, Any]:
        """
        重置安卓容器

        Args:
            ip: IP地址
            name: API名称

        Returns:
            API详细信息
            格式: {"code": 200, "msg": ""}
        """
        endpoint = f"/dc_api/v1/reset/{ip}/{name}"
        return self._make_request("GET", endpoint)
    def pull_images(self, ip: str, image_addr: str) -> Dict[str, Any]:
        """
        拉取镜像

        Args:
            ip: IP地址
            image_addr: 镜像地址

        Returns:
            API详细信息
            格式: {"code": 200, "msg": ""}
        """
        endpoint = f"/dc_api/v1/pull_image/{ip}"
        params = {"image_addr": image_addr}

        return self._make_request("POST", endpoint, params=params)
    def pull_images2(self, ip: str, image_addr: str) -> Dict[str, Any]:
        """
        拉取镜像

        Args:
            ip: IP地址
            image_addr: 镜像地址

        Returns:
            API详细信息
            格式: {"code": 200, "msg": ""}
        """
        endpoint = f"/dc_api/v1/pull_image2/{ip}"
        params = {"image_addr": image_addr}

        return self._make_request("POST", endpoint, params=params)
    def del_container(self, ip: str, name: str) -> Dict[str, Any]:
        """
        删除容器

        Args:
            ip: IP地址
            name: 容器名称

        Returns:
            API详细信息
            格式: {"code": 200, "msg": ""}
        """
        endpoint = f"/dc_api/v1/remove/{ip}/{name}"
        return self._make_request("GET", endpoint)

    def modify_device_info(
        self,
        ip: str,
        name: str,
        act: str,
        abroad: Optional[int] = None,
        model_id: Optional[int] = None,
        lang: Optional[str] = None,
        userip: Optional[str] = None,
        is_async: Optional[int] = None,
    ) -> Dict[str, Any]:
        """
        修改设备信息

        Args:
            ip: 3588主机ip地址
            name: 容器名称
            act: 操作类型，1=获取机型字典表，2=随机设备机型
            abroad: 可选，1表示海外设备机型随机
            model_id: 可选，获取机型列表字典中指定的机型参数
            lang: 可选，随机后的指定语言 zh中文/en英语/fr法语/th泰国/vi越南/ja日本/ko韩国/lo老挝/in印尼
            userip: 可选，指定环境对应ip所在的区域，如果不指定默认为当前云机的ip，注意：不支持域名仅支持ipv4地址
            is_async: 可选，1表示使用异步的方式请求结果，能够准确的获取请求结果(推荐使用)但是仅仅支持最新的镜像

        Returns:
            设备信息修改结果
            格式: {"code": 200, "msg": ""}

        Examples:
            # 获取机型列表
            client.modify_device_info("192.168.1.100", "container1", "1")
            
            # 海外机型随机
            client.modify_device_info("192.168.1.100", "container1", "2", abroad=1)
            
            # 设置指定机型
            client.modify_device_info("192.168.1.100", "container1", "2", model_id=1)
        """
        endpoint = f"/and_api/v1/devinfo/{ip}/{name}/{act}"
        params = {}
        
        if abroad is not None:
            params["abroad"] = abroad
        if model_id is not None:
            params["model_id"] = model_id
        if lang is not None:
            params["lang"] = lang
        if userip is not None:
            params["userip"] = userip
        if is_async is not None:
            params["is_async"] = is_async

        # 设置默认超时时间为60秒
        return self._make_request("GET", endpoint, params=params, timeout=60)

def create_client(
    base_url: str = "http://127.0.0.1:5000", timeout: int = 30,
) -> MYTAPIClient:
    """
    创建MYT API客户端实例

    Args:
        base_url: API服务器基础URL
        timeout: 请求超时时间

    Returns:
        MYTAPIClient实例
    """
    return MYTAPIClient(base_url=base_url, timeout=timeout)
