import numpy as np


def augment_image(  im1,                    # Image 1
                    im2,                    # Image 2
                    augs,                   # Augments to select from
                    probs,                  # Probabilities to use in each augments parameters
                    alphas,                 # The alpha values for each mix
                    mix_p = None            # Probability of selecting an augment
                    ):


    # Choose a random index to select an augment and its respective parametes

    idx = np.random.choice(len(augs), p=mix_p)
    aug = augs[idx]
    prob = float(probs[idx])
    alpha = float(alphas[idx])

    mask = None


    # Do not augment the images, just return copies of the originals


    if aug == "none":
        im1_aug, im2_aug = im1.clone(), im2.clone()



    elif aug == "cutblur":
        im1_aug, im2_aug = cutblur( im1.clone(), im2.clone(),
                                    prob=prob, alpha=alpha )



    return im1_aug, im2_aug, mask, aug


def apply_augment(  im1,                    # Image 1
                    im2,                    # Image 2
                    augs,                   # Augments to select from
                    probs,                  # Probabilities to use in each augments parameters
                    alphas,                 # The alpha values for each mix
                    mix_p = None,           # Probability of selecting an augment
                    aux_prob=None, 
                    aux_alpha=None,
                    ):
    
    return augment_image(im1, im2, augs, probs, alphas, mix_p = None)
    

# CutBlur Code

def cutblur(im1, im2,prob,alpha):

    # If alpha doesnt make sense or if the number is higher than the probability
    # no not perform the augmentation.

    if alpha <= 0 or np.random.rand(1) >= prob:
        return im1, im2

    # Generate a random cut ratio

    cut_ratio = np.random.randn() * 0.01 + alpha

    # The boundaries of the patch to cut and paste

    h, w = im2.size(2), im2.size(3)                     # get height and width
    ch, cw = np.int(h*cut_ratio), np.int(w*cut_ratio)   # get height and width of patch

    cy = np.random.randint(0, h-ch+1)                   # random y cordinate of patch
    cx = np.random.randint(0, w-cw+1)                   # random x cordinate of patch



    # Perform the cutblur

    if np.random.random() > 0.5:
        im2[..., cy:cy+ch, cx:cx+cw] = im1[..., cy:cy+ch, cx:cx+cw]
    else:
        im2_aug = im1.clone()
        im2_aug[..., cy:cy+ch, cx:cx+cw] = im2[..., cy:cy+ch, cx:cx+cw]
        im2 = im2_aug

    return im1 , im2
