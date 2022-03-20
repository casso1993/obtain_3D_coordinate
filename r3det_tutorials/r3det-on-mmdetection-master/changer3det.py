import torch
pretrained_weights  = torch.load('epoch_24.pth')

num_class = 5
pretrained_weights['state_dict']['bbox_head.retina_cls.weight'].resize_(num_class*21, 256, 3, 3)
pretrained_weights['state_dict']['bbox_head.retina_cls.bias'].resize_(num_class*21)

pretrained_weights['state_dict']['refine_head.0.retina_cls.weight'].resize_(num_class, 256, 3, 3)
pretrained_weights['state_dict']['refine_head.0.retina_cls.bias'].resize_(num_class)

pretrained_weights['state_dict']['refine_head.1.retina_cls.weight'].resize_(num_class, 256, 3, 3)
pretrained_weights['state_dict']['refine_head.1.retina_cls.bias'].resize_(num_class)

torch.save(pretrained_weights, "r3det_r50_fpn_2x_%d.pth"%num_class)