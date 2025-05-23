import torch
import torchvision.transforms as transforms
from torchvision.models import resnet50
from PIL import Image

def extract_features(image_path):
    # 加载预训练的 ResNet-50 模型
    model = resnet50(pretrained=True)
    model.eval()

    # 图像预处理
    preprocess = transforms.Compose([
        transforms.Resize(256),
        transforms.CenterCrop(224),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
    ])

    # 读取图像
    img = Image.open(image_path)
    img_t = preprocess(img)
    batch_t = torch.unsqueeze(img_t, 0)

    # 提取特征
    with torch.no_grad():
        out = model(batch_t)

    # 将特征向量转换为一维数组并返回
    return out.flatten().numpy()
