import torch
import click
import warnings
from segment_anything.modeling import Sam
from segment_anything import sam_model_registry
from segment_anything.utils.onnx import SamOnnxModel

def export(sam: Sam, model_output_path: str):
    device = torch.device("cpu")
    print(f"Using device: {device}")
    sam = sam.to(device)
    onnx_model = SamOnnxModel(sam, return_single_mask=True)

    dynamic_axes = {
        "point_coords": {1: "num_points"},
        "point_labels": {1: "num_points"},
    }

    embed_dim = sam.prompt_encoder.embed_dim
    embed_size = sam.prompt_encoder.image_embedding_size
    mask_input_size = [4 * x for x in embed_size]
    dummy_inputs = {
        "image_embeddings": torch.randn(1, embed_dim, *embed_size, dtype=torch.float),
        "point_coords": torch.randint(low=0, high=1024, size=(1, 5, 2), dtype=torch.float),
        "point_labels": torch.randint(low=0, high=4, size=(1, 5), dtype=torch.float),
        "mask_input": torch.randn(1, 1, *mask_input_size, dtype=torch.float),
        "has_mask_input": torch.tensor([1], dtype=torch.float),
        "orig_im_size": torch.tensor([1500, 2250], dtype=torch.float),
    }
    output_names = ["masks", "iou_predictions", "low_res_masks"]

    with warnings.catch_warnings():
        warnings.filterwarnings("ignore", category=torch.jit.TracerWarning)
        warnings.filterwarnings("ignore", category=UserWarning)
        with open(model_output_path, "wb") as f:
            torch.onnx.export(
                onnx_model,
                tuple(dummy_inputs.values()),
                f,
                export_params=True,
                verbose=False,
                opset_version=17,
                do_constant_folding=True,
                input_names=list(dummy_inputs.keys()),
                output_names=output_names,
                dynamic_axes=dynamic_axes,
            )   


@click.command()
@click.option('--model',
              default='vit_h',
              help='model name',
              type=click.Choice(['vit_b', 'vit_l', 'vit_h']))
@click.option('--model_path', default='static/model/sam_vit_h_4b8939.pth', help='model path')
@click.option('--model_output_path', default='static/model/sam_vit_b_01ec64.onnx', help='model output path')
def main(model: str, model_path: str, model_output_path: str):
    sam = sam_model_registry[model](checkpoint=model_path)
    export(sam, model_output_path)

if __name__ == '__main__':
    main()      
