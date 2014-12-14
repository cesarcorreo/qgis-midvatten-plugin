<!DOCTYPE qgis PUBLIC 'http://mrcc.com/qgis.dtd' 'SYSTEM'>
<qgis version="2.6.1-Brighton" minimumScale="0" maximumScale="1e+08" hasScaleBasedVisibilityFlag="0">
  <edittypes>
    <edittype widgetv2type="TextEdit" name="obsid">
      <widgetv2config IsMultiline="0" fieldEditable="1" UseHtml="0" labelOnTop="1"/>
    </edittype>
    <edittype widgetv2type="DateTime" name="date_time">
      <widgetv2config fieldEditable="1" calendar_popup="1" allow_null="1" display_format="yyyy-MM-dd HH:mm:ss" field_format="yyyy-MM-dd HH:mm:ss" labelOnTop="1"/>
    </edittype>
    <edittype widgetv2type="Range" name="meas">
      <widgetv2config AllowNull="1" fieldEditable="1" Step="1" Style="SpinBox" labelOnTop="1" Min="0" Max="100000" Suffix=" m from reference point"/>
    </edittype>
    <edittype widgetv2type="Range" name="h_toc">
      <widgetv2config AllowNull="1" fieldEditable="1" Step="1" Style="SpinBox" labelOnTop="1" Min="0" Max="1000000" Suffix=" meter above sea level"/>
    </edittype>
    <edittype widgetv2type="Range" name="level_masl">
      <widgetv2config AllowNull="1" fieldEditable="1" Step="1" Style="SpinBox" labelOnTop="1" Min="0" Max="1000000" Suffix=" meter above sea level"/>
    </edittype>
    <edittype widgetv2type="TextEdit" name="comment">
      <widgetv2config IsMultiline="0" fieldEditable="1" UseHtml="0" labelOnTop="1"/>
    </edittype>
  </edittypes>
  <editform></editform>
  <editforminit>form_logics.w_levels_form_open</editforminit>
  <featformsuppress>1</featformsuppress>
  <annotationform>.</annotationform>
  <editorlayout>tablayout</editorlayout>
  <excludeAttributesWMS/>
  <excludeAttributesWFS/>
  <attributeEditorForm>
    <attributeEditorContainer name="water level measurement">
      <attributeEditorField index="0" name="obsid"/>
      <attributeEditorField index="1" name="date_time"/>
      <attributeEditorField index="2" name="meas"/>
      <attributeEditorField index="3" name="h_toc"/>
      <attributeEditorField index="4" name="level_masl"/>
      <attributeEditorField index="5" name="comment"/>
    </attributeEditorContainer>
  </attributeEditorForm>
  <attributeactions/>
</qgis>
