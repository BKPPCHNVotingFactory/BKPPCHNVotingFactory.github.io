$(document).ready(function () {
  // 获取数据
  let voteArr = [];

  $.ajaxSettings.async = false;
  $.getJSON(`../json/vote.json?random=${Math.random()}`, (resJ) => {
    voteArr = resJ.res;
  });

  // console.log(voteArr);

  baseDom = $("#statistical_json");
  for (let i = 0; i < voteArr.length; i++) {
    let item = voteArr[i];
    let statisticalListDom = $("<div/>", {
      class: "statistical_list",
    }).append(
      $("<header/>", {
        html: `${item.date} Vote`,
      })
    );
    for (let j = 0; j < item.data.length; j++) {
      let item_data = item.data[j];

      let tbodyDom = $("<tbody/>");
      for (let h = 0; h < item_data.list.length; h++) {
        let item_list = item_data.list[h];
        tbodyDom.append(
          $("<tr/>", {
            class: item_list.active_item == 1 ? "active_item" : "",
          }).append(
            $("<th/>", {
              scope: "row",
              html: h + 1,
            }),
            $("<td/>", {
              html: item_list.item_name,
            }),
            $("<td/>", {
              html: item_list.score,
            }),
            $("<td/>", {
              html: item_list.weight,
            })
          )
        );
      }

      let sectionDim = $("<section/>", {
        class: "group_header",
      }).append(
        $("<div/>", {
          class: "group_title",
        }).append(
          $("<span/>", {
            html: item_data.category_name,
          }),
          $("<span/>", {
            html: `总票数：${item_data.sumScore} 票`,
          })
        ),
        $("<div/>", {
          class: "group_vote_list",
        }).append(
          $("<table/>", {
            class: "table table-dark",
          }).append(
            $("<thead/>").append(
              $("<tr/>").append(
                $("<th/>", {
                  scope: "col",
                  html: "排名",
                }),
                $("<th/>", {
                  scope: "col",
                  html: "姓名",
                }),
                $("<th/>", {
                  scope: "col",
                  html: "票数",
                }),
                $("<th/>", {
                  scope: "col",
                  html: "比例",
                })
              )
            ),
            tbodyDom
          )
        )
      );

      statisticalListDom.append(sectionDim);
    }

    baseDom.append(statisticalListDom);
  }
  // $("#statistical_json").
});
