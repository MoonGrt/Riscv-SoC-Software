
def module_template(module_type, module_name, inport):
    # inport = 
    if len(inport) == 1:
        # 单输入端口
        inport = single_inport(module_name, inport)
    else:
        # 多输入端口
        inport = multi_inport(module_name, inport)
    template = f"""
    //--------------------------------------------------------------------------
    // {module_type}
    //--------------------------------------------------------------------------
    {inport}
    wire        {module_name}_post_vs;  // Processed Image data vs valid signal
    wire        {module_name}_post_de;  // Processed Image data output/capture enable clock
    wire [23:0] {module_name}_post_data;  // Processed Image output
    {module_type} {module_name} (
        .clk      (clk),
        .rst_n    (rst_n),
        .mode     ({module_name}_mode),  // 00: bypass, 01: gaussian, 10: median, 11: mean

        .pre_vs   ({module_name}_post_vs),
        .pre_de   ({module_name}_post_de),
        .pre_data ({module_name}_post_data),
        .post_vs  ({module_name}_post_vs),
        .post_de  ({module_name}_post_de),
        .post_data({module_name}_post_data)
    );
    """
    return template

def single_inport(module_name, inport):
    # 定义一个函数，用于生成输入端口
    return f"""wire        {module_name}_pre_vs = {inport[0].split('.')[1]}_post_vs;  // Prepared Image data vs valid signal
    wire        {module_name}_pre_de = {inport[0].split('.')[1]}_post_vs;  // Prepared Image data output/capture enable clock
    wire [23:0] {module_name}_pre_data = {inport[0].split('.')[1]}_post_vs;  // Prepared Image output"""

def multi_inport(module_name, inport):
    # 定义一个函数，用于生成多个输入端口
    # 生成case语句的模板
    case_statements = ""
    for i, port in enumerate(inport, start=1):
        case_statements += f"""
                2'b{"%02d" % i}: begin
                    {module_name}_pre_vs   = {port.split('.')[1].lower()}_post_vs;
                    {module_name}_pre_de   = {port.split('.')[1].lower()}_post_de;
                    {module_name}_pre_data = {port.split('.')[1].lower()}_post_data;
                end"""
    template = f"""    wire        {module_name}_pre_vs;  // Prepared Image data vs valid signal
    wire        {module_name}_pre_de;  // Prepared Image data output/capture enable clock
    wire [23:0] {module_name}_pre_data;  // Prepared Image output
    always @ (*) begin
        if (~rst_n) begin
            {module_name}_pre_vs   = 1'b0;
            {module_name}_pre_de   = 1'b0;
            {module_name}_pre_data = 24'd0;
        end else begin
            case ({module_name}_mode)
                {case_statements}
                default: begin
                    {module_name}_pre_vs   = 1'b0;
                    {module_name}_pre_de   = 1'b0;
                    {module_name}_pre_data = 24'd0;
                end
            endcase
        end
    end
    """
    return template

def VP_Gen(VPFunc, output_file="AhbVP.v"):
    VP = ""
    for module, port in VPFunc.items():
        # 遍历VPFunc列表，依次生成每个功能模块
        module_type = module.split('.')[0]
        module_name = module.split('.')[1]
        # 解析模块名称和类型
        if module_type == 'VI' or module_type == 'VO':
            # 输入输出模块
            pass
        else:
            VP += module_template(module_type=module_type, module_name=module_name, inport=port["in"])
    print(VP)
    with open(output_file, 'w') as f:
        f.write(VP)


if __name__ == "__main__":
    VPFunc = {'VI.VI': {'in': [], 'out': ['Cutter.Cutter']}, 'Cutter.Cutter': {'in': ['VI.VI'], 'out': ['Filter.Filter']}, 
               'Filter.Filter': {'in': ['Cutter.Cutter'], 'out': ['Color.Color', 'Scaler.Scaler']}, 'Color.Color': {'in': ['Filter.Filter'], 'out': ['Bit.Bit', 'Edger.Edger']}, 
               'Scaler.Scaler': {'in': ['Filter.Filter'], 'out': ['Filler.Filler']}, 'Bit.Bit': {'in': ['Color.Color'], 'out': ['Filler.Filler']}, 
               'Edger.Edger': {'in': ['Color.Color'], 'out': ['Filler.Filler']}, 'Filler.Filler': {'in': ['Scaler.Scaler', 'Bit.Bit', 'Edger.Edger'], 'out': ['VO.VO']}, 
               'VO.VO': {'in': ['Filler.Filler'], 'out': []}}  # 定义一个空的函数变量，用于保存DVP功能模块
    VP_Gen(VPFunc)
