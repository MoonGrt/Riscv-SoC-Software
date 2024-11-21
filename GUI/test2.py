def multi_inport(module_name, inport):
    # 输入端口个数
    in_cnt = len(inport)

    # 生成case语句的模板
    case_statements = ""
    for i, port in enumerate(inport, start=1):
        case_statements += f"""
                2'b{"%02d" % i}: begin
                    {module_name}_pre_clk  = clk_vp;  // 示例时钟信号
                    {module_name}_pre_vs   = {port.lower()}_post_vs;
                    {module_name}_pre_de   = {port.lower()}_post_de;
                    {module_name}_pre_data = {port.lower()}_post_data;
                end
        """

    # 完整的always块
    full_template = f"""
    wire        {module_name}_pre_vs;  // Prepared Image data vs valid signal
    wire        {module_name}_pre_de;  // Prepared Image data output/capture enable clock
    wire [23:0] {module_name}_pre_data;  // Prepared Image output
    always @ (*) begin
        if (~rst_n) begin
            {module_name}_pre_clk  = 1'b0;
            {module_name}_pre_vs   = 1'b0;
            {module_name}_pre_de   = 1'b0;
            {module_name}_pre_data = 24'd0;
        end else begin
            case (vp_mode)
                {case_statements}
                default: begin
                    {module_name}_pre_clk  = 1'b0;
                    {module_name}_pre_vs   = 1'b0;
                    {module_name}_pre_de   = 1'b0;
                    {module_name}_pre_data = 24'd0;
                end
            endcase
        end
    end
    """
    return full_template

module_name = "filler"
inport = ["Scaler", "Bit", "Edger"]

generated_code = multi_inport(module_name, inport)
print(generated_code)
