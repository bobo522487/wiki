

# RViz 中的 MoveIt 快速入门[](https://moveit.picknik.ai/humble/doc/tutorials/quickstart_in_rviz/quickstart_in_rviz_tutorial.html#moveit-quickstart-in-rviz)

![../../../_images/rviz_plugin_head.png](https://moveit.picknik.ai/humble/_images/rviz_plugin_head.png)

本教程将教您如何使用 RViz 和 MoveIt Display 插件在 MoveIt 中创建运动计划。 Rviz 是 ROS 中的主要可视化工具，也是调试机器人的非常有用的工具。 MoveIt Display 插件允许您设置虚拟环境（规划场景）、交互式地创建机器人的开始和目标状态、测试各种运动规划器以及可视化输出。让我们开始吧！

## 入门[](https://moveit.picknik.ai/humble/doc/tutorials/quickstart_in_rviz/quickstart_in_rviz_tutorial.html#getting-started)

如果您尚未执行此操作，请确保您已完成[入门](https://moveit.picknik.ai/humble/doc/tutorials/getting_started/getting_started.html)或我们的[Docker 指南](https://moveit.picknik.ai/humble/doc/how_to_guides/how_to_setup_docker_containers_in_ubuntu.html)中的步骤。截至 2022 年 9 月 26 日，确保您已按照此处所述启用 Cyclone DDS。

## 第 1 步：启动演示并配置插件[](https://moveit.picknik.ai/humble/doc/tutorials/quickstart_in_rviz/quickstart_in_rviz_tutorial.html#step-1-launch-the-demo-and-configure-the-plugin)

- 启动演示：

  ```
  ros2 launch moveit2_tutorials demo.launch.py rviz_config:=panda_moveit_config_demo_empty.rviz
  ```

  

- 如果您是第一次执行此操作，您应该在 RViz 中看到一个空的世界，并且必须添加运动规划插件：

  - 您应该在 RViz 中看到一个空的世界：

  [![A](https://moveit.picknik.ai/humble/_images/rviz_empty.png)](https://moveit.picknik.ai/humble/_images/rviz_empty.png)

  - 在 RViz 显示选项卡中，按*添加*：

  [![乙](https://moveit.picknik.ai/humble/_images/rviz_click_add.png)](https://moveit.picknik.ai/humble/_images/rviz_click_add.png)

  - 从 moveit_ros_visualization 文件夹中，选择“MotionPlanning”作为 DisplayType。按“确定”。

  [![C](https://moveit.picknik.ai/humble/_images/rviz_plugin_motion_planning_add.png)](https://moveit.picknik.ai/humble/_images/rviz_plugin_motion_planning_add.png)

  - 您现在应该在 RViz 中看到 Panda 机器人：

  [![D](https://moveit.picknik.ai/humble/_images/rviz_start.png)](https://moveit.picknik.ai/humble/_images/rviz_start.png)

- 加载运动规划插件后，我们就可以对其进行配置。在“显示”子窗口的“全局选项”选项卡中，将“**固定框架**”字段设置为`/panda_link0`
- 现在，您可以开始为您的机器人（本例中为 Panda）配置插件。单击“显示”中的“MotionPlanning”。
  - 确保**机器人描述**字段设置为`robot_description`。
  - 确保**规划场景主题**字段设置为`/monitored_planning_scene`。单击主题名称以显示主题名称下拉列表。
  - 确保**计划路径**下的**轨迹主题**设置为。`/display_planned_path`
  - 在**计划请求**中，将**计划组**更改为`panda_arm`。您还可以在左下角的 MotionPlanning 面板中看到这一点。

[![../../../_images/rviz_plugin_start.png](https://moveit.picknik.ai/humble/_images/rviz_plugin_start.png)](https://moveit.picknik.ai/humble/_images/rviz_plugin_start.png)

## 第 2 步：玩可视化机器人[](https://moveit.picknik.ai/humble/doc/tutorials/quickstart_in_rviz/quickstart_in_rviz_tutorial.html#step-2-play-with-the-visualized-robots)

有四种不同的重叠可视化：

1. 机器人在`/monitored_planning_scene`规划环境中的配置（默认处于活动状态）。
2. 机器人的规划路径（默认处于活动状态）。
3. 绿色：运动规划的开始状态（默认禁用）。
4. 橙色：运动规划的目标状态（默认处于活动状态）。

可以使用复选框打开和关闭每个可视化的显示状态：

1. **使用“场景机器人”**树菜单中的**“显示机器人视觉”**复选框规划场景机器人。
2. **使用“规划路径”**树菜单中的**“显示机器人视觉”**复选框来规划路径。
3. **使用规划请求**树菜单中的**查询开始状态**复选框的开始状态。
4. **使用计划请求**树菜单中的**查询目标状态**复选框的目标状态。

- 使用所有这些复选框来打开和关闭不同的可视化效果。

[![../../../_images/rviz_plugin_visualize_robots.png](https://moveit.picknik.ai/humble/_images/rviz_plugin_visualize_robots.png)](https://moveit.picknik.ai/humble/_images/rviz_plugin_visualize_robots.png)

## 第三步：与熊猫互动[](https://moveit.picknik.ai/humble/doc/tutorials/quickstart_in_rviz/quickstart_in_rviz_tutorial.html#step-3-interact-with-the-panda)

对于接下来的步骤，我们只需要场景机器人、开始状态和目标状态：

1. 选中**规划路径**树菜单中的**显示机器人视觉复选框**
2. 取消选中**场景机器人**树菜单中的**显示机器人视觉复选框**
3. **选中规划请求**树菜单中的查询**目标状态**复选框。
4. **选中规划请求**树菜单中的查询**开始状态**复选框。

现在应该有两个交互式标记。与橙色手臂相对应的一个标记将用于设置运动规划的“目标状态”，与绿色手臂相对应的另一个标记将用于设置运动规划的“开始状态”。如果您没有看到交互标记，请按RViz 顶部菜单中的“**交互” （注意：某些工具可能会被隐藏，请按顶部菜单中的****“+”**添加**交互**工具，如下所示）。

[![../../../_images/rviz_plugin_interact.png](https://moveit.picknik.ai/humble/_images/rviz_plugin_interact.png)](https://moveit.picknik.ai/humble/_images/rviz_plugin_interact.png)

您现在应该能够使用这些标记来拖动手臂并更改其方向。尝试一下！

### 进入碰撞状态[](https://moveit.picknik.ai/humble/doc/tutorials/quickstart_in_rviz/quickstart_in_rviz_tutorial.html#moving-into-collision)

对于本部分，隐藏计划路径和目标状态：

1. 取消选中**规划路径**树菜单中的**显示机器人视觉复选框**
2. 取消**选中规划请求**树菜单中的查询**目标状态**复选框。

现在，只有“开始状态”（绿色臂）应该可见。尝试将手臂移动到其两个连杆相互碰撞的配置。 （如果您发现这很困难，请确保未选中 MotionPlanning 插件的规划选项卡下的“使用碰撞感知 IK”复选框。）执行此操作后，发生碰撞的链接将变为红色。

[![../../../_images/rviz_plugin_collision.png](https://moveit.picknik.ai/humble/_images/rviz_plugin_collision.png)](https://moveit.picknik.ai/humble/_images/rviz_plugin_collision.png)

现在，选中“使用碰撞感知 IK”复选框，并再次尝试将两个链接移动到彼此碰撞。勾选该复选框后，IK 解算器将继续尝试为所需的末端执行器姿势找到无碰撞解决方案。如果未选中，解算器将允许解决方案中发生碰撞。无论复选框的状态如何，发生冲突的链接始终会显示为红色。

[![../../../_images/rviz_plugin_collision_aware_ik_checkbox.png](https://moveit.picknik.ai/humble/_images/rviz_plugin_collision_aware_ik_checkbox.png)](https://moveit.picknik.ai/humble/_images/rviz_plugin_collision_aware_ik_checkbox.png)

### 移出可到达的工作空间[](https://moveit.picknik.ai/humble/doc/tutorials/quickstart_in_rviz/quickstart_in_rviz_tutorial.html#moving-out-of-reachable-workspace)

请注意当您尝试将末端执行器移出其可到达的工作空间时会发生什么。

[![../../../_images/rviz_plugin_invalid.png](https://moveit.picknik.ai/humble/_images/rviz_plugin_invalid.png)](https://moveit.picknik.ai/humble/_images/rviz_plugin_invalid.png)

在进入下一部分之前，重新启用计划路径和目标状态：

1. 选中**规划路径**树菜单中的**显示机器人视觉复选框**
2. **选中规划请求**树菜单中的查询**目标状态**复选框。

### 移动关节或在零空间中[](https://moveit.picknik.ai/humble/doc/tutorials/quickstart_in_rviz/quickstart_in_rviz_tutorial.html#moving-joints-or-in-null-space)

您可以使用**“关节”**选项卡移动 7-DOF 机器人的单个关节和冗余关节。尝试移动“零空间探索”滑块，如下面的动画所示。

<video width="700px" controls="true" autoplay="true" loop="true" __idm_id__="327681" style="box-sizing: border-box; display: inline-block;"></video>

## 第 4 步：对 Panda 使用运动规划[](https://moveit.picknik.ai/humble/doc/tutorials/quickstart_in_rviz/quickstart_in_rviz_tutorial.html#step-4-use-motion-planning-with-the-panda)

- 现在，您可以在 MoveIt RViz 插件中使用 Panda 开始运动规划。
  - 将开始状态移动到所需位置。
  - 将目标状态移动到另一个所需位置。
  - 确保这两种状态都不会与机器人本身发生碰撞。
  - 确保计划路径被可视化。另请选中 **“规划路径”**树菜单中的**“显示轨迹”**复选框。
- 在**“MotionPlanning”窗口的****“规划”**选项卡下，按**“规划”**按钮。您应该能够看到手臂移动和轨迹的可视化。

[![../../../_images/rviz_plugin_planned_path.png](https://moveit.picknik.ai/humble/_images/rviz_plugin_planned_path.png)](https://moveit.picknik.ai/humble/_images/rviz_plugin_planned_path.png)

### 内省轨迹路点[](https://moveit.picknik.ai/humble/doc/tutorials/quickstart_in_rviz/quickstart_in_rviz_tutorial.html#introspecting-trajectory-waypoints)

您可以在 RViz 中逐点直观地内省轨迹。

- 从“*面板*”菜单中，选择“*轨迹 - 轨迹滑块*”。您将在 RViz 上看到一个新的滑块面板。
- 设置您的目标姿势，然后运行*Plan*。
- 使用“*滑块*”面板进行播放，例如移动滑块，按“*播放*”按钮。

注意：将 EEF 设置为新目标后，请务必在运行*“播放”*之前运行*“计划”* ——否则您将看到上一个目标的航路点（如果有）。

[![../../../_images/rviz_plugin_slider.png](https://moveit.picknik.ai/humble/_images/rviz_plugin_slider.png)](https://moveit.picknik.ai/humble/_images/rviz_plugin_slider.png)

### 规划笛卡尔运动[](https://moveit.picknik.ai/humble/doc/tutorials/quickstart_in_rviz/quickstart_in_rviz_tutorial.html#plan-cartesian-motions)

如果激活“使用笛卡尔路径”复选框，机器人将尝试在笛卡尔空间中线性移动末端执行器。

[![../../../_images/rviz_plan_free.png](https://moveit.picknik.ai/humble/_images/rviz_plan_free.png)](https://moveit.picknik.ai/humble/_images/rviz_plan_free.png) [![../../../_images/rviz_plan_cartesian.png](https://moveit.picknik.ai/humble/_images/rviz_plan_cartesian.png)](https://moveit.picknik.ai/humble/_images/rviz_plan_cartesian.png)

### 执行轨迹、调整速度[](https://moveit.picknik.ai/humble/doc/tutorials/quickstart_in_rviz/quickstart_in_rviz_tutorial.html#executing-trajectories-adjusting-speed)

计划成功后点击“计划并执行”或“执行”会将轨迹发送给机器人——在本教程中，由于您使用了`demo.launch`，因此仅模拟机器人。

最初，默认速度和加速度缩放为`0.1`机器人最大值的 10% ( )。您可以在如下所示的“规划”选项卡中更改这些缩放系数，或在`moveit_config`机器人的（在`joint_limits.yaml`）中更改这些默认值。

[![../../../_images/rviz_plugin_collision_aware_ik_checkbox.png](https://moveit.picknik.ai/humble/_images/rviz_plugin_collision_aware_ik_checkbox.png)](https://moveit.picknik.ai/humble/_images/rviz_plugin_collision_aware_ik_checkbox.png)

## 下一步[](https://moveit.picknik.ai/humble/doc/tutorials/quickstart_in_rviz/quickstart_in_rviz_tutorial.html#next-steps)

### RViz 可视化工具[](https://moveit.picknik.ai/humble/doc/tutorials/quickstart_in_rviz/quickstart_in_rviz_tutorial.html#rviz-visual-tools)

许多教程都用来`moveit_visual_tools`逐步完成演示。在继续学习下一个教程之前，最好启用**RvizVisualToolsGui**。

从“*面板*”菜单中，选择“*添加新面板*”。从菜单中选择“ *RvizVisualToolsGui* ”并单击“确定”。您将看到添加到 RViz 的新面板。

[![../../../_images/rviz_add_rviz_visual_tools.png](https://moveit.picknik.ai/humble/_images/rviz_add_rviz_visual_tools.png)](https://moveit.picknik.ai/humble/_images/rviz_add_rviz_visual_tools.png) [![../../../_images/rviz_panels.png](https://moveit.picknik.ai/humble/_images/rviz_panels.png)](https://moveit.picknik.ai/humble/_images/rviz_panels.png)

### 保存您的配置[](https://moveit.picknik.ai/humble/doc/tutorials/quickstart_in_rviz/quickstart_in_rviz_tutorial.html#saving-your-configuration)

RViz 使您能够将配置保存在.您应该在继续学习下一个教程之前执行此操作。如果您选择以新名称保存配置，则可以使用以下命令来使用和引用您的配置文件：`File->Save Config``File->Save Config As`

```
ros2 launch moveit2_tutorials demo.launch.py rviz_config:=your_rviz_config.rviz
```



替换`your_rviz_config.rviz`为您保存的文件的名称`moveit2_tutorials/doc/tutorials/quickstart_in_rviz/launch/`并构建工作区以便可以找到它。

### 下一个教程[](https://moveit.picknik.ai/humble/doc/tutorials/quickstart_in_rviz/quickstart_in_rviz_tutorial.html#next-tutorial)

在[您的第一个 MoveIt 项目](https://moveit.picknik.ai/humble/doc/tutorials/your_first_project/your_first_project.html)中，您将使用 MoveIt 创建一个 C++ 程序来计划和执行移动。