import torch
import torch.nn as nn
import torch.nn.functional as F
from einops import rearrange, repeat

class Residual(nn.Module):
    def __init__(self, fn):
        super().__init__()
        self.fn = fn
    def forward(self, x, **kwargs):
        return self.fn(x, **kwargs) + x


class PreNorm(nn.Module):
    def __init__(self, dim, fn):
        super().__init__()
        self.norm = nn.LayerNorm(dim)
        self.fn = fn
    def forward(self, x, **kwargs):
        return self.fn(self.norm(x), **kwargs)

class FeedForward(nn.Module):
    def __init__(self, dim, hidden_dim, dropout = 0.):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(dim, hidden_dim),
            nn.GELU(),
            nn.Dropout(dropout),
            nn.Linear(hidden_dim, dim),
            nn.Dropout(dropout)
        )
    def forward(self, x):
        return self.net(x)

class Attention(nn.Module):
    def __init__(self, dim, heads = 8, dim_head = 64, dropout = 0.):
        super().__init__()
        inner_dim = dim_head *  heads
        self.heads = heads
        self.scale = dim ** -0.5

        self.to_qkv = nn.Linear(dim, inner_dim * 3, bias = False)
        self.to_out = nn.Sequential(
            nn.Linear(inner_dim, dim),
            nn.Dropout(dropout)
        )

    def forward(self, x, mask = None):
        b, n, _, h = *x.shape, self.heads
        qkv = self.to_qkv(x).chunk(3, dim = -1)

        q, k, v = map(lambda t: rearrange(t, 'b n (h d) -> b h n d', h = h), qkv)
        dots = torch.einsum('bhid,bhjd->bhij', q, k) * self.scale
        mask_value = -torch.finfo(dots.dtype).max
        #embed()
        if mask is not None:
            mask = F.pad(mask.flatten(1), (1, 0), value = True)
            assert mask.shape[-1] == dots.shape[-1], 'mask has incorrect dimensions'
            mask = mask[:, None, :] * mask[:, :, None]
            dots.masked_fill_(~mask, mask_value)
            del mask

        attn = dots.softmax(dim=-1)

        out = torch.einsum('bhij,bhjd->bhid', attn, v)
        out = rearrange(out, 'b h n d -> b n (h d)')
        out =  self.to_out(out)

        return out

class Transformer(nn.Module):
    def __init__(self, dim, depth, heads, dim_head, mlp_dim, dropout):
        super().__init__()
        self.layers = nn.ModuleList([])
        for _ in range(depth):
            self.layers.append(nn.ModuleList([
                Residual(PreNorm(dim, Attention(dim, heads = heads, dim_head = dim_head, dropout = dropout))),
                Residual(PreNorm(dim, FeedForward(dim, mlp_dim, dropout = dropout)))
            ]))
    def forward(self, x, mask = None):
        for attn, ff in self.layers:
            x = attn(x, mask = mask)
            #embed()
            x = ff(x)
        return x

class FusionModel(nn.Module):
    def __init__(self, v_input_size = 512, hidden_size=512, num_layers=2, num_classes=2):
        super(FusionModel, self).__init__()
        # self.lstm = nn.LSTM(v_input_size, hidden_size, num_layers, batch_first=True)
        self.fusion_fc = nn.Linear(hidden_size, num_classes)
        self.softmax = nn.Softmax(dim=1)
        self.cls_token = nn.Parameter(torch.randn(1, 1, v_input_size))
        self.dropout = nn.Dropout(0.1)

        # print("MM self.dropout: ", self.dropout)
        self.transformer = Transformer(dim=v_input_size, depth=6, heads=8, dim_head=64, mlp_dim=2048, dropout=0.1)
        # self.transformer = Transformer(dim=v_input_size, depth=6, heads=8, dim_head=64, mlp_dim=2048, dropout=0.1)

        self.fc = nn.Linear(hidden_size, num_classes)

        
    def forward(self, v):
        cls_tokens = repeat(self.cls_token, '() n d -> b n d', b = v.shape[0])
        v = torch.cat((cls_tokens, v), dim=1)   #B,61,512
        v = self.dropout(v)
        # print("B v.shape: ", v.shape)
        v = self.transformer(v)                 #B,61,512
        # print("A v.shape: ", v.shape)
        v_tokens = v.clone()                     #B,61,512
        v = v[:, 0]                             #B,512
        # print("v[:, 0].shape: ", v.shape)

        out = self.fc(v)  # 取最後一個時間步的輸出
        
        return out, v_tokens
