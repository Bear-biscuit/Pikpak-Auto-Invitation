# coding:utf-8
import hashlib
import json
import random
import time
import uuid
import requests
from PIL import Image
from io import BytesIO
import base64
import os


def ca_f_encrypt(frames, index, pid, use_proxy=False, proxies=None):
    url = "https://api.kiteyuan.info/cafEncrypt"

    payload = json.dumps({
        "frames": frames,
        "index": index,
        "pid": pid
    })
    headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
            "Connection": "keep-alive",
            'Content-Type': 'application/json',
            "Upgrade-Insecure-Requests": "1",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "none",
            "Sec-Fetch-User": "?1"
        }

    try:
        # response = requests.request("POST", url, headers=headers, data=payload, proxies=proxies if use_proxy else None)
        response = requests.request("POST", url, headers=headers, data=payload, proxies=None)
        response.raise_for_status()
        if not response.text:
            print(f"API响应为空: {url}")
            return {"f": "", "ca": ["", "", "", ""]}
        
        # 解析响应以确保与 text.py 行为一致
        result = json.loads(response.text)
        if "f" not in result or "ca" not in result:
            print(f"API响应缺少关键字段: {result}")
            return {"f": "", "ca": ["", "", "", ""]}
        return result
    except requests.exceptions.RequestException as e:
        print(f"API请求失败: {e}")
        if use_proxy:
            print(f"当前使用的代理: {proxies}")
        return {"f": "", "ca": ["", "", "", ""]}
    except json.JSONDecodeError as e:
        print(f"JSON解析错误: {e}, 响应内容: {response.text}")
        return {"f": "", "ca": ["", "", "", ""]}


def image_parse(image, frames, use_proxy=False, proxies=None):
    url = "https://api.kiteyuan.info/imageParse"

    payload = json.dumps({
        "image": image,
        "frames": frames
    })
    headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
            "Connection": "keep-alive",
            'Content-Type': 'application/json',
            "Upgrade-Insecure-Requests": "1",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "none",
            "Sec-Fetch-User": "?1"
        }

    try:
        # response = requests.request("POST", url, headers=headers, data=payload, proxies=proxies if use_proxy else None)
        response = requests.request("POST", url, headers=headers, data=payload, proxies=None)
        response.raise_for_status()  # 检查HTTP状态码
        if not response.text:
            print(f"API响应为空: {url}")
            return {"best_index": 0}  # 返回一个默认值
        
        # 解析响应以确保与 text.py 行为一致
        result = json.loads(response.text)
        if "best_index" not in result:
            print(f"API响应缺少best_index字段: {result}")
            return {"best_index": 0}
        return result
    except requests.exceptions.RequestException as e:
        print(f"API请求失败: {e}")
        if use_proxy:
            print(f"当前使用的代理: {proxies}")
        return {"best_index": 0}  # 返回一个默认值
    except json.JSONDecodeError as e:
        print(f"JSON解析错误: {e}, 响应内容: {response.text}")
        return {"best_index": 0}  # 返回一个默认值


def sign_encrypt(code, captcha_token, rtc_token, use_proxy=False, proxies=None):
    url = "https://api.kiteyuan.info/signEncrypt"

    # 检查 code 是否为空或 None
    if not code:
        print("code 参数为空，无法进行加密")
        return {"request_id": "", "sign": ""}

    # 如果 code 是字符串而不是对象，则直接使用
    if isinstance(code, str):
        payload_data = code
    else:
        try:
            payload_data = json.dumps(code)
        except (TypeError, ValueError) as e:
            print(f"code 参数序列化失败: {e}")
            return {"request_id": "", "sign": ""}

    try:
        payload = json.dumps({
            "code": payload_data,
            "captcha_token": captcha_token,
            "rtc_token": rtc_token
        })
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
            "Connection": "keep-alive",
            'Content-Type': 'application/json',
            "Upgrade-Insecure-Requests": "1",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "none",
            "Sec-Fetch-User": "?1"
        }

        # response = requests.request("POST", url, headers=headers, data=payload, proxies=proxies if use_proxy else None, timeout=30)
        response = requests.request("POST", url, headers=headers, data=payload, proxies=None, timeout=30)
        response.raise_for_status()
        if not response.text:
            print(f"API响应为空: {url}")
            return {"request_id": "", "sign": ""}
        
        # 解析响应以确保与 text.py 行为一致
        result = json.loads(response.text)
        if "request_id" not in result or "sign" not in result:
            print(f"API响应缺少关键字段: {result}")
            return {"request_id": "", "sign": ""}
        return result
    except requests.exceptions.RequestException as e:
        print(f"API请求失败: {e}")
        if use_proxy:
            print(f"当前使用的代理: {proxies}")
        return {"request_id": "", "sign": ""}
    except json.JSONDecodeError as e:
        print(f"JSON解析错误: {e}, 响应内容: {response.text}")
        return {"request_id": "", "sign": ""}
    except Exception as e:
        print(f"未知错误: {e}")
        return {"request_id": "", "sign": ""}


def d_encrypt(pid, device_id, f, use_proxy=False, proxies=None):
    url = "https://api.kiteyuan.info/dEncrypt"

    payload = json.dumps({
        "pid": pid,
        "device_id": device_id,
        "f": f
    })
    headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
            "Connection": "keep-alive",
            'Content-Type': 'application/json',
            "Upgrade-Insecure-Requests": "1",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "none",
            "Sec-Fetch-User": "?1"
        }

    try:
        # response = requests.request("POST", url, headers=headers, data=payload, proxies=proxies if use_proxy else None)
        response = requests.request("POST", url, headers=headers, data=payload, proxies=None)
        response.raise_for_status()
        if not response.text:
            print(f"API响应为空: {url}")
            return ""
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"API请求失败: {e}")
        if use_proxy:
            print(f"当前使用的代理: {proxies}")
        return ""


# md5加密算法
def captcha_sign_encrypt(encrypt_string, salts):
    for salt in salts:
        encrypt_string = hashlib.md5((encrypt_string + salt["salt"]).encode("utf-8")).hexdigest()
    return encrypt_string


def captcha_image_parse(pikpak, device_id):
    try:
        # 获取frames信息
        frames_info = pikpak.gen()
        if not frames_info or not isinstance(frames_info, dict) or "pid" not in frames_info or "frames" not in frames_info:
            print("获取frames_info失败，返回内容:", frames_info)
            return {"response_data": {"result": "reject"}, "pid": "", "traceid": ""}
        if "traceid" not in frames_info:
            frames_info["traceid"] = ""
        # 下载验证码图片
        captcha_image = image_download(device_id, frames_info["pid"], frames_info["traceid"], pikpak.use_proxy, pikpak.proxies)
        if not captcha_image:
            print("图片下载失败")
            return {"response_data": {"result": "reject"}, "pid": frames_info["pid"], "traceid": frames_info["traceid"]}
        
        # 读取图片数据并转换为 PIL.Image
        img = Image.open(BytesIO(captcha_image))
        
        # 将图片转换为 Base64 编码
        buffered = BytesIO()
        img.save(buffered, format="PNG")  # 可根据图片格式调整 format
        base64_image = base64.b64encode(buffered.getvalue()).decode()
        
        # 获取最佳滑块位置
        best_index = image_parse(base64_image, frames_info["frames"], pikpak.use_proxy, pikpak.proxies)
        if "best_index" not in best_index:
            print("图片分析失败, 返回内容:", best_index)
            return {"response_data": {"result": "reject"}, "pid": frames_info["pid"], "traceid": frames_info["traceid"]}
        
        # 滑块加密
        json_data = ca_f_encrypt(frames_info["frames"], best_index["best_index"], frames_info["pid"], pikpak.use_proxy, pikpak.proxies)
        if "f" not in json_data or "ca" not in json_data:
            print("加密计算失败, 返回内容:", json_data)
            return {"response_data": {"result": "reject"}, "pid": frames_info["pid"], "traceid": frames_info["traceid"]}
        
        f = json_data['f']
        npac = json_data['ca']
        
        # d加密
        d = d_encrypt(frames_info["pid"], device_id, f, pikpak.use_proxy, pikpak.proxies)
        if not d:
            print("d_encrypt失败")
            return {"response_data": {"result": "reject"}, "pid": frames_info["pid"], "traceid": frames_info["traceid"]}
        
        # 验证
        verify2 = pikpak.image_verify(frames_info["pid"], frames_info["traceid"], f, npac[0], npac[1], npac[2], npac[3], d)
        
        return {
            "response_data": verify2,
            "pid": frames_info["pid"],
            "traceid": frames_info["traceid"],
        }
    except Exception as e:
        print(f"滑块验证过程中出错: {e}")
        import traceback
        traceback.print_exc()
        return {"response_data": {"result": "reject"}, "pid": "", "traceid": ""}


def image_download(device_id, pid, traceid, use_proxy=False, proxies=None):
    url = f"https://user.mypikpak.com/pzzl/image?deviceid={device_id}&pid={pid}&traceid={traceid}"

    headers = {
        'pragma': 'no-cache',
        'priority': 'u=1, i'
    }

    try:
        response = requests.get(url, headers=headers, proxies=proxies if use_proxy else None)
        response.raise_for_status()
        if response.status_code == 200:
            return response.content  # 直接返回图片的二进制数据
        else:
            print(f"下载失败，状态码: {response.status_code}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"图片下载失败: {e}")
        if use_proxy:
            print(f"当前使用的代理: {proxies}")
        return None


def ramdom_version():
    version_list = [
        {
            "v": "1.42.6",
            "algorithms": [{"alg": "md5", "salt": "frupTFdxwcJ5mcL3R8"},
                           {"alg": "md5", "salt": "jB496fSFfbWLhWyqV"},
                           {"alg": "md5", "salt": "xYLtzn8LT5h3KbAalCjc/Wf"},
                           {"alg": "md5", "salt": "PSHSbm1SlxbvkwNk4mZrJhBZ1vsHCtEdm3tsRiy1IPUnqi1FNB5a2F"},
                           {"alg": "md5", "salt": "SX/WvPCRzgkLIp99gDnLaCs0jGn2+urx7vz/"},
                           {"alg": "md5", "salt": "OGdm+dgLk5EpK4O1nDB+Z4l"},
                           {"alg": "md5", "salt": "nwtOQpz2xFLIE3EmrDwMKe/Vlw2ubhRcnS2R23bwx9wMh+C3Sg"},
                           {"alg": "md5", "salt": "FI/9X9jbnTLa61RHprndT0GkVs18Chd"}]

        },
        {
            "v": "1.47.1",
            "algorithms": [{'alg': 'md5', 'salt': 'Gez0T9ijiI9WCeTsKSg3SMlx'}, {'alg': 'md5', 'salt': 'zQdbalsolyb1R/'},
                           {'alg': 'md5', 'salt': 'ftOjr52zt51JD68C3s'},
                           {'alg': 'md5', 'salt': 'yeOBMH0JkbQdEFNNwQ0RI9T3wU/v'},
                           {'alg': 'md5', 'salt': 'BRJrQZiTQ65WtMvwO'},
                           {'alg': 'md5', 'salt': 'je8fqxKPdQVJiy1DM6Bc9Nb1'},
                           {'alg': 'md5', 'salt': 'niV'}, {'alg': 'md5', 'salt': '9hFCW2R1'},
                           {'alg': 'md5', 'salt': 'sHKHpe2i96'},
                           {'alg': 'md5', 'salt': 'p7c5E6AcXQ/IJUuAEC9W6'}, {'alg': 'md5', 'salt': ''},
                           {'alg': 'md5', 'salt': 'aRv9hjc9P+Pbn+u3krN6'},
                           {'alg': 'md5', 'salt': 'BzStcgE8qVdqjEH16l4'},
                           {'alg': 'md5', 'salt': 'SqgeZvL5j9zoHP95xWHt'},
                           {'alg': 'md5', 'salt': 'zVof5yaJkPe3VFpadPof'}]
        },
        {
            "v": "1.48.3",
            "algorithms": [{'alg': 'md5', 'salt': 'aDhgaSE3MsjROCmpmsWqP1sJdFJ'},
                           {'alg': 'md5', 'salt': '+oaVkqdd8MJuKT+uMr2AYKcd9tdWge3XPEPR2hcePUknd'},
                           {'alg': 'md5', 'salt': 'u/sd2GgT2fTytRcKzGicHodhvIltMntA3xKw2SRv7S48OdnaQIS5mn'},
                           {'alg': 'md5', 'salt': '2WZiae2QuqTOxBKaaqCNHCW3olu2UImelkDzBn'},
                           {'alg': 'md5', 'salt': '/vJ3upic39lgmrkX855Qx'},
                           {'alg': 'md5', 'salt': 'yNc9ruCVMV7pGV7XvFeuLMOcy1'},
                           {'alg': 'md5', 'salt': '4FPq8mT3JQ1jzcVxMVfwFftLQm33M7i'},
                           {'alg': 'md5', 'salt': 'xozoy5e3Ea'}]
        },
        {
            "v": "1.49.3",
            "algorithms": [{'alg': 'md5', 'salt': '7xOq4Z8s'}, {'alg': 'md5', 'salt': 'QE9/9+IQco'},
                           {'alg': 'md5', 'salt': 'WdX5J9CPLZp'}, {'alg': 'md5', 'salt': 'NmQ5qFAXqH3w984cYhMeC5TJR8j'},
                           {'alg': 'md5', 'salt': 'cc44M+l7GDhav'}, {'alg': 'md5', 'salt': 'KxGjo/wHB+Yx8Lf7kMP+/m9I+'},
                           {'alg': 'md5', 'salt': 'wla81BUVSmDkctHDpUT'},
                           {'alg': 'md5', 'salt': 'c6wMr1sm1WxiR3i8LDAm3W'},
                           {'alg': 'md5', 'salt': 'hRLrEQCFNYi0PFPV'},
                           {'alg': 'md5', 'salt': 'o1J41zIraDtJPNuhBu7Ifb/q3'},
                           {'alg': 'md5', 'salt': 'U'}, {'alg': 'md5', 'salt': 'RrbZvV0CTu3gaZJ56PVKki4IeP'},
                           {'alg': 'md5', 'salt': 'NNuRbLckJqUp1Do0YlrKCUP'},
                           {'alg': 'md5', 'salt': 'UUwnBbipMTvInA0U0E9'},
                           {'alg': 'md5', 'salt': 'VzGc'}]
        },
        {
            "v": "1.51.2",
            "algorithms": [{'alg': 'md5', 'salt': 'vPjelkvqcWoCsQO1CnkVod8j2GbcE0yEHEwJ3PKSKW'},
                           {'alg': 'md5', 'salt': 'Rw5aO9MHuhY'}, {'alg': 'md5', 'salt': 'Gk111qdZkPw/xgj'},
                           {'alg': 'md5', 'salt': '/aaQ4/f8HNpyzPOtIF3rG/UEENiRRvpIXku3WDWZHuaIq+0EOF'},
                           {'alg': 'md5', 'salt': '6p1gxZhV0CNuKV2QO5vpibkR8IJeFURvqNIKXWOIyv1A'},
                           {'alg': 'md5', 'salt': 'gWR'},
                           {'alg': 'md5', 'salt': 'iPD'}, {'alg': 'md5', 'salt': 'ASEm+P75YfKzQRW6eRDNNTd'},
                           {'alg': 'md5', 'salt': '2fauuwVCxLCpL/FQ/iJ5NpOPb7gRZs0EWJwe/2YNPQr3ore+ZiIri6s/tYayG'}]
        }
    ]
    return version_list[0]
    # return random.choice(version_list)


def random_rtc_token():
    # 生成 8 组 16 进制数，每组 4 位，使用冒号分隔
    ipv6_parts = ["{:04x}".format(random.randint(0, 0xFFFF)) for _ in range(8)]
    ipv6_address = ":".join(ipv6_parts)
    return ipv6_address


class PikPak:
    def __init__(self, invite_code, client_id, device_id, version, algorithms, email, rtc_token,
                 client_secret, package_name, use_proxy=False, proxy_http=None, proxy_https=None):
        # 初始化实例属性
        self.invite_code = invite_code  # 邀请码
        self.client_id = client_id  # 客户端ID
        self.device_id = device_id  # 设备ID
        self.timestamp = 0  # 时间戳
        self.algorithms = algorithms  # 版本盐值
        self.version = version  # 版本
        self.email = email  # 邮箱
        self.rtc_token = rtc_token  # RTC Token
        self.captcha_token = ""  # Captcha Token
        self.client_secret = client_secret  # Client Secret
        self.user_id = ""  # 用户ID
        self.access_token = ""  # 登录令牌
        self.refresh_token = ""  # 刷新令牌
        self.verification_token = ""  # Verification Token
        self.captcha_sign = ""  # Captcha Sign
        self.verification_id = ""  # Verification ID
        self.package_name = package_name  # 客户端包名
        self.use_proxy = use_proxy  # 是否使用代理

        # 代理配置
        if use_proxy:
            self.proxies = {
                "http": proxy_http or "http://127.0.0.1:7890",
                "https": proxy_https or "http://127.0.0.1:7890",
            }
        else:
            self.proxies = None

    def send_request(self, method, url, headers=None, params=None, json_data=None, data=None, use_proxy=None):
        headers = headers or {}
        # 如果未指定use_proxy，则使用类的全局设置
        use_proxy = self.use_proxy if use_proxy is None else use_proxy
        
        # 确保当use_proxy为True时，有可用的代理配置
        if use_proxy and not self.proxies:
            # 如果类的use_proxy为True但proxies未设置，使用默认代理
            proxies = {
                "http": "http://127.0.0.1:7890",
                "https": "http://127.0.0.1:7890"
            }
        else:
            proxies = self.proxies if use_proxy else None

        try:
            response = requests.request(
                method=method,
                url=url,
                headers=headers,
                params=params,
                json=json_data,
                data=data,
                proxies=proxies,
                timeout=30  # 添加超时设置
            )
            response.raise_for_status()  # 检查HTTP状态码
            
            print(response.text)
            try:
                return response.json()
            except json.JSONDecodeError:
                return response.text
        except requests.exceptions.RequestException as e:
            print(f"请求失败: {url}, 错误: {e}")
            if use_proxy:
                print(f"当前使用的代理: {proxies}")
            # 返回一个空的响应对象
            return {}

    def gen(self):
        url = "https://user.mypikpak.com/pzzl/gen"
        params = {"deviceid": self.device_id, "traceid": ""}
        headers = {"Host": "user.mypikpak.com", "accept": "application/json, text/plain, */*"}
        response = self.send_request("GET", url, headers=headers, params=params)
        # 检查响应是否有效
        if not response or not isinstance(response, dict) or "pid" not in response or "traceid" not in response:
            print(f"gen请求返回无效响应: {response}")
        return response

    def image_verify(self, pid, trace_id, f, n, p, a, c, d):
        url = "https://user.mypikpak.com/pzzl/verify"
        params = {"pid": pid, "deviceid": self.device_id, "traceid": trace_id, "f": f, "n": n, "p": p, "a": a, "c": c,
                  "d": d}
        headers = {"Host": "user.mypikpak.com", "accept": "application/json, text/plain, */*"}
        response = self.send_request("GET", url, headers=headers, params=params)
        # 检查响应是否有效
        if not response or not isinstance(response, dict) or "result" not in response:
            print(f"image_verify请求返回无效响应: {response}")
            return {"result": "reject"}
        return response

    def executor(self):
        url = "https://api-drive.mypikpak.com/captcha-jsonp/v2/executor?callback=handleJsonpResult_" + str(int(time.time() * 1000))
        headers = {'pragma': 'no-cache', 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'}
        
        try:
            # 使用普通 requests 而不是 self.send_request 以获取原始响应
            response = requests.get(url, headers=headers, proxies=self.proxies if self.use_proxy else None, timeout=30)
            response.raise_for_status()  # 检查 HTTP 状态码
            
            content = response.text
            print(f"executor 原始响应: {content}")
            
            # 如果内容为空，直接返回空字符串
            if not content:
                print("executor 响应内容为空")
                return ""
            
            # 处理 JSONP 响应格式
            if "handleJsonpResult" in content:
                # 提取 JSON 部分，JSONP 格式通常是 callback(json数据)
                start_index = content.find('(')
                end_index = content.rfind(')')
                
                if start_index != -1 and end_index != -1:
                    json_str = content[start_index + 1:end_index]
                    # 有时 JSONP 响应中包含反引号，需要去除
                    if json_str.startswith('`') and json_str.endswith('`'):
                        json_str = json_str[1:-1]
                    
                    return json_str
                else:
                    print(f"无法从JSONP响应中提取有效内容: {content}")
                    return ""
            elif isinstance(content, str) and (content.startswith('{') or content.startswith('[')):
                # 可能是直接返回的 JSON 字符串
                return content
            else:
                print(f"未知的响应格式: {content}")
                return ""
        except requests.exceptions.RequestException as e:
            print(f"执行 executor 请求失败: {e}")
            return ""
        except Exception as e:
            print(f"解析 executor 响应失败: {e}")
            return ""

    def report(self, request_id, sign, pid, trace_id):
        url = "https://user.mypikpak.com/credit/v1/report"
        params = {
            "deviceid": self.device_id,
            "captcha_token": self.captcha_token,
            "request_id": request_id,
            "sign": sign,
            "type": "pzzlSlider",
            "result": 0,
            "data": pid,
            "traceid": trace_id,
            "rtc_token": self.rtc_token
        }
        headers = {'pragma': 'no-cache', 'priority': 'u=1, i'}
        response = self.send_request("GET", url, params=params, headers=headers)
        # 检查响应是否有效
        if not response or not isinstance(response, dict) or "captcha_token" not in response:
            print(f"report请求返回无效响应: {response}")
        else:
            self.captcha_token = response.get('captcha_token')
        return response

    def verification(self):
        url = 'https://user.mypikpak.com/v1/auth/verification'
        params = {"email": self.email, "target": "ANY", "usage": "REGISTER", "locale": "zh-CN",
                  "client_id": self.client_id}
        headers = {'host': 'user.mypikpak.com', 'x-captcha-token': self.captcha_token, 'x-device-id': self.device_id,
                   "x-client-id": self.client_id}
        response = self.send_request("POST", url, headers=headers, data=params)
        # 检查响应是否有效
        if not response or not isinstance(response, dict) or "verification_id" not in response:
            print(f"verification请求返回无效响应: {response}")
        else:
            self.verification_id = response.get('verification_id')
        return response

    def verify_post(self, verification_code):
        url = "https://user.mypikpak.com/v1/auth/verification/verify"
        params = {"client_id": self.client_id}
        payload = {"client_id": self.client_id, "verification_id": self.verification_id,
                   "verification_code": verification_code}
        headers = {"X-Device-Id": self.device_id}
        response = self.send_request("POST", url, headers=headers, json_data=payload, params=params)
        # 检查响应是否有效
        if not response or not isinstance(response, dict) or "verification_token" not in response:
            print(f"verify_post请求返回无效响应: {response}")
        else:
            self.verification_token = response.get('verification_token')
        return response

    def init(self, action):
        self.refresh_captcha_sign()
        url = "https://user.mypikpak.com/v1/shield/captcha/init"
        params = {"client_id": self.client_id}
        payload = {
            "action": action,
            "captcha_token": self.captcha_token,
            "client_id": self.client_id,
            "device_id": self.device_id,
            "meta": {
                "captcha_sign": "1." + self.captcha_sign,
                "user_id": self.user_id,
                "package_name": self.package_name,
                "client_version": self.version,
                "email": self.email,
                "timestamp": self.timestamp
            }
        }
        headers = {"x-device-id": self.device_id}
        response = self.send_request("POST", url, headers=headers, json_data=payload, params=params)
        # 检查响应是否有效
        if not response or not isinstance(response, dict) or "captcha_token" not in response:
            print(f"init请求返回无效响应: {response}")
        else:
            self.captcha_token = response.get('captcha_token')
        return response

    def signup(self, name, password, verification_code):
        url = "https://user.mypikpak.com/v1/auth/signup"
        params = {"client_id": self.client_id}
        payload = {
            "captcha_token": self.captcha_token,
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "email": self.email,
            "name": name,
            "password": password,
            "verification_code": verification_code,
            "verification_token": self.verification_token
        }
        headers = {"X-Device-Id": self.device_id}
        response = self.send_request("POST", url, headers=headers, json_data=payload, params=params)
        # 检查响应是否有效
        if not response or not isinstance(response, dict):
            print(f"signup请求返回无效响应: {response}")
        else:
            self.access_token = response.get('access_token', '')
            self.refresh_token = response.get('refresh_token', '')
            self.user_id = response.get('sub', '')
        return response

    def activation_code(self):
        url = "https://api-drive.mypikpak.com/vip/v1/order/activation-code"
        payload = {"activation_code": self.invite_code, "data": {}}
        headers = {
            "Host": "api-drive.mypikpak.com",
            "authorization": "Bearer " + self.access_token,
            "x-captcha-token": self.captcha_token,
            "x-device-id": self.device_id,
            'x-system-language': "ko",
            'content-type': 'application/json'
        }
        response = self.send_request("POST", url, headers=headers, json_data=payload)
        # 检查响应是否有效
        if not response or not isinstance(response, dict):
            print(f"activation_code请求返回无效响应: {response}")
        return response

    def files_task(self, task_link):
        url = "https://api-drive.mypikpak.com/drive/v1/files"
        payload = {
            "kind": "drive#file",
            "folder_type": "DOWNLOAD",
            "upload_type": "UPLOAD_TYPE_URL",
            "url": {"url": task_link},
            "params": {"with_thumbnail": "true", "from": "manual"}
        }
        headers = {
            "Authorization": "Bearer " + self.access_token,
            "x-device-id": self.device_id,
            "x-captcha-token": self.captcha_token,
            "Content-Type": "application/json"
        }
        response = self.send_request("POST", url, headers=headers, json_data=payload)
        # 检查响应是否有效
        if not response or not isinstance(response, dict):
            print(f"files_task请求返回无效响应: {response}")
        return response

    def refresh_captcha_sign(self):
        self.timestamp = str(int(time.time()) * 1000)
        encrypt_string = self.client_id + self.version + self.package_name + self.device_id + self.timestamp
        self.captcha_sign = captcha_sign_encrypt(encrypt_string, self.algorithms)


def save_account_info(name, account_info):
    with open("./account/" + name + ".json", "w", encoding="utf-8") as f:
        json.dump(account_info, f, ensure_ascii=False, indent=4)


def test_proxy(proxy_url):
    """测试代理连接是否可用"""
    test_url = "https://mypikpak.com"  # 改为 PikPak 的网站，更可能连通
    proxies = {
        "http": proxy_url,
        "https": proxy_url
    }
    
    try:
        response = requests.get(test_url, proxies=proxies, timeout=10)  # 增加超时时间
        response.raise_for_status()
        print(f"代理连接测试成功: {proxy_url}")
        return True
    except Exception as e:
        print(f"代理连接测试失败: {proxy_url}, 错误: {e}")
        return False


# 程序运行主函数
def main():
    try:
        # 1、初始化参数
        current_version = ramdom_version()
        version = current_version['v']
        algorithms = current_version['algorithms']
        client_id = "YNxT9w7GMdWvEOKa"
        client_secret = "dbw2OtmVEeuUvIptb1Coyg"
        package_name = "com.pikcloud.pikpak"
        device_id = str(uuid.uuid4()).replace("-", "")
        rtc_token = random_rtc_token()
        print(f"当前版本:{version} 设备号:{device_id} 令牌:{rtc_token}")
        
        # 询问用户是否使用代理
        use_proxy_input = input('是否启用代理(y/n)：').strip().lower()
        use_proxy = use_proxy_input == 'y' or use_proxy_input == 'yes'
        
        proxy_http = None
        proxy_https = None
        
        if use_proxy:
            # 询问用户是否使用默认代理
            default_proxy = input('是否使用默认代理地址 http://127.0.0.1:7890 (y/n)：').strip().lower()
            if default_proxy == 'y' or default_proxy == 'yes':
                proxy_url = "http://127.0.0.1:7890"
                print("已启用代理，使用默认地址:", proxy_url)
                
                # 测试默认代理连接
                if not test_proxy(proxy_url):
                    retry = input("默认代理连接测试失败，是否继续使用(y/n)：").strip().lower()
                    if retry != 'y' and retry != 'yes':
                        print("已取消代理设置，将直接连接")
                        use_proxy = False
                        proxy_url = None
                
                if use_proxy:
                    proxy_http = proxy_url
                    proxy_https = proxy_url
            else:
                # 用户自定义代理地址和端口
                proxy_host = input('请输入代理主机地址 (默认127.0.0.1): ').strip()
                proxy_host = proxy_host if proxy_host else '127.0.0.1'
                
                proxy_port = input('请输入代理端口 (默认7890): ').strip()
                proxy_port = proxy_port if proxy_port else '7890'
                
                proxy_protocol = input('请输入代理协议 (http/https/socks5，默认http): ').strip().lower()
                proxy_protocol = proxy_protocol if proxy_protocol in ['http', 'https', 'socks5'] else 'http'
                
                proxy_url = f"{proxy_protocol}://{proxy_host}:{proxy_port}"
                print(f"已设置代理地址: {proxy_url}")
                
                # 测试自定义代理连接
                if not test_proxy(proxy_url):
                    retry = input("自定义代理连接测试失败，是否继续使用(y/n)：").strip().lower()
                    if retry != 'y' and retry != 'yes':
                        print("已取消代理设置，将直接连接")
                        use_proxy = False
                        proxy_url = None
                
                if use_proxy:
                    proxy_http = proxy_url
                    proxy_https = proxy_url
        else:
            print("未启用代理，直接连接")
        
        invite_code = input('请输入你的邀请码：')
        email = input("请输入注册用的邮箱：")
        # 2、实例化PikPak类，传入代理设置
        pikpak = PikPak(invite_code, client_id, device_id, version, algorithms, email, rtc_token, client_secret,
                        package_name, use_proxy=use_proxy, proxy_http=proxy_http, proxy_https=proxy_https)
        
        # 3、刷新timestamp，加密sign值。
        init_result = pikpak.init("POST:/v1/auth/verification")
        if not init_result or not isinstance(init_result, dict) or "captcha_token" not in init_result:
            print("初始化失败，请检查网络连接或代理设置")
            input("按任意键退出程序")
            return
            
        # 4、图片滑块分析
        max_attempts = 5  # 最大尝试次数
        captcha_result = None
        
        for attempt in range(max_attempts):
            print(f"尝试滑块验证 ({attempt+1}/{max_attempts})...")
            try:
                captcha_result = captcha_image_parse(pikpak, device_id)
                print(captcha_result)
                
                if captcha_result and "response_data" in captcha_result and captcha_result['response_data'].get('result') == 'accept':
                    print("滑块验证成功!")
                    break
                else:
                    print('滑块验证失败, 正在重新尝试...')
                    time.sleep(2)  # 延迟2秒再次尝试
            except Exception as e:
                print(f"滑块验证过程出错: {e}")
                import traceback
                traceback.print_exc()
                time.sleep(2)  # 出错后延迟2秒再次尝试
        
        if not captcha_result or "response_data" not in captcha_result or captcha_result['response_data'].get('result') != 'accept':
            print("滑块验证失败，达到最大尝试次数")
            input("按任意键退出程序")
            return
            
        # 5、滑块验证加密
        try:
            executor_info = pikpak.executor()
            if not executor_info:
                print("获取executor信息失败")
                input("按任意键退出程序")
                return
                
            sign_encrypt_info = sign_encrypt(executor_info, pikpak.captcha_token, rtc_token, pikpak.use_proxy, pikpak.proxies)
            if not sign_encrypt_info or "request_id" not in sign_encrypt_info or "sign" not in sign_encrypt_info:
                print("签名加密失败")
                print(f"executor_info: {executor_info}")
                print(f"captcha_token: {pikpak.captcha_token}")
                print(f"rtc_token: {rtc_token}")
                input("按任意键退出程序")
                return
                
            # 更新 captcha_token
            pikpak.report(sign_encrypt_info['request_id'], sign_encrypt_info['sign'], captcha_result['pid'],
                        captcha_result['traceid'])
            
            # 发送邮箱验证码
            verification_result = pikpak.verification()
            if not verification_result or not isinstance(verification_result, dict) or "verification_id" not in verification_result:
                print("请求验证码失败")
                input("按任意键退出程序")
                return
        except Exception as e:
            print(f"验证过程出错: {e}")
            import traceback
            traceback.print_exc()
            input("按任意键退出程序")
            return
            
        # 6、提交验证码
        verification_code = input("请输入接收到的验证码：")
        pikpak.verify_post(verification_code)
        
        # 7、刷新timestamp，加密sign值
        pikpak.init("POST:/v1/auth/signup")
        
        # 8、注册登录
        name = email.split("@")[0]
        password = "zhiyuan233"
        pikpak.signup(name, password, verification_code)
        
        # 9、填写邀请码
        pikpak.activation_code()
        
        # 准备账号信息
        account_info = {
            "version": pikpak.version,
            "device_id": pikpak.device_id,
            "email": pikpak.email,
            "captcha_token": pikpak.captcha_token,
            "access_token": pikpak.access_token,
            "refresh_token": pikpak.refresh_token,
            "user_id": pikpak.user_id,
            "timestamp": pikpak.timestamp,
            "password": password,
            "name": name
        }
        
        print("请保存好账号信息备用：", json.dumps(account_info, indent=4, ensure_ascii=False))
        
        # 确认是否保存账号信息
        save_info = input("是否保存账号信息到文件(y/n)：").strip().lower()
        if save_info == 'y' or save_info == 'yes':
            try:
                # 创建account目录（如果不存在）
                if not os.path.exists("./account"):
                    os.makedirs("./account")
                save_account_info(name, account_info)
                print(f"账号信息已保存到 ./account/{name}.json")
            except Exception as e:
                print(f"保存账号信息失败: {e}")
        
        input("运行完成，回车结束程序：")
    except KeyboardInterrupt:
        print("\n程序被用户中断")
    except Exception as e:
        print(f"程序运行出错: {e}")
        import traceback
        traceback.print_exc()
        input("按任意键退出程序")


if __name__ == "__main__":
    print("开发者声明：免费转载需标注出处：B站-纸鸢花的花语，此工具仅供交流学习和技术分析，严禁用于任何商业牟利行为。（包括但不限于倒卖、二改倒卖、引流、冒充作者、广告植入...）")
    main()
